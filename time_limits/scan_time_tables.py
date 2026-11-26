#!/usr/bin/env python3
"""Find candidate Nikon EXPEED 4 movie time-limit tables in a decrypted module.

The known E4 table is 30 little-endian u32 values in milliseconds, e.g.
[600000, 1200000, 600000, ..., 1799000].  This scanner looks for a run of
`--count` u32 values drawn from a set of plausible limits; it is read-only.

Usage:
    python scan_time_tables.py --module b1010_115a.bin
    python scan_time_tables.py --module b860_102.bin --count 30 --min-score 26
"""

import argparse
import json
import struct
from pathlib import Path

import numpy as np

DEFAULT_ALLOWED = (
    60000,     # 1 min
    180000,    # 3 min
    300000,    # 5 min
    600000,    # 10 min
    900000,    # 15 min
    1200000,   # 20 min
    1500000,   # 25 min
    1799000,   # 29:59
    1800000,   # 30 min
    3599000,   # 59:59
    3600000,   # 60 min
)


def scan(module, count, min_score, allowed):
    stride = 4
    usable = len(module) // stride * stride
    a = np.frombuffer(module[:usable], dtype="<u4")
    mask = np.isin(a, allowed).astype(np.int32)
    window = np.ones(count, dtype=np.int32)
    score = np.convolve(mask, window, "valid")
    hits = np.where(score >= min_score)[0]

    raw = []
    for i in hits:
        vals = [int(x) for x in a[i:i + count]]
        if len(set(vals)) < 2:
            continue
        raw.append({
            "offset": int(i) * stride,
            "score": int(score[i]),
            "values": vals,
            "next_u32": int(a[i + count]) if i + count < len(a) else None,
        })

    # A real table produces many overlapping windows.  Group them and keep the
    # best-scoring (then lowest-offset) window in each group.
    groups = []
    cur = []
    last = None
    for r in raw:
        if last is not None and r["offset"] - last > count * stride:
            groups.append(cur)
            cur = []
        cur.append(r)
        last = r["offset"]
    if cur:
        groups.append(cur)

    out = []
    for group in groups:
        best = max(group, key=lambda r: (r["score"], -r["offset"]))
        best["offset"] = "0x%X" % best["offset"]
        out.append(best)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--module", required=True)
    ap.add_argument("--count", type=int, default=30)
    ap.add_argument("--min-score", type=int, default=28)
    ap.add_argument("--json", help="write results as JSON")
    args = ap.parse_args(argv)

    module = Path(args.module).read_bytes()
    results = scan(module, args.count, args.min_score, DEFAULT_ALLOWED)

    print("module %s (%d bytes)" % (args.module, len(module)))
    print("candidates: %d (count=%d, min-score=%d)" % (len(results), args.count, args.min_score))
    for r in results:
        vals = r["values"]
        mn = min(vals) / 1000.0
        mx = max(vals) / 1000.0
        print(
            "  0x%-8s score=%2d  %d..%d s  next=0x%X"
            % (r["offset"][2:], r["score"], int(mn), int(mx), r["next_u32"] or 0)
        )
        print("      %s" % ", ".join(str(v) for v in vals))

    if args.json:
        Path(args.json).write_text(
            json.dumps({"module": args.module, "candidates": results},
                       indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("wrote %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
