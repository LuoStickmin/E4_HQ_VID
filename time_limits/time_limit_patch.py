#!/usr/bin/env python3
"""Set every entry of a Nikon EXPEED 4 movie time-limit table to a fixed value.

The E4 movie time-limit table is a contiguous array of little-endian u32
milliseconds (600000 = 10 min, 1200000 = 20 min, 1799000 = 29:59).  This tool
verifies the stock table and rewrites every entry; it does not touch any other
byte.

Read-only by default: without --out it only checks.  With --out it writes a
patched module and verifies that the diff is confined to the table.

Usage:
    python time_limit_patch.py --module b1010_115a.bin \
        --profile profiles/d750_0115_time59.json --check
    python time_limit_patch.py --module b1010_115a.bin \
        --profile profiles/d750_0115_time59.json \
        --out b1010_115a.time59.bin --json report.json

The module is expected to be the decrypted main module (for D750 1.15:
b1010_115a.bin).  Repacking the module back into a camera firmware is a
separate step (E4_HQ_VID/tools/repack_firmware.py).
"""

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path


def u32(data, off):
    return struct.unpack_from("<I", data, off)[0]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fmt_ms(ms):
    s = ms / 1000.0
    return "%d:%06.3f (%d ms)" % (int(s // 60), s % 60, ms)


def load_profile(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    table = doc["table"]
    off = int(str(table["offset"]), 0)
    count = int(table["count"])
    stride = int(table.get("stride", 4))
    expected = [int(x) for x in doc["expected"]]
    if len(expected) != count:
        raise SystemExit(
            "profile error: expected has %d values, table.count is %d"
            % (len(expected), count)
        )
    if stride != 4:
        raise SystemExit("profile error: only u32 tables (stride=4) are supported")
    return doc, off, count, stride, expected


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Patch an EXPEED 4 movie time-limit table (u32 ms)."
    )
    ap.add_argument("--module", required=True, help="decrypted main module")
    ap.add_argument("--profile", required=True, help="model profile JSON")
    ap.add_argument(
        "--seconds",
        type=int,
        help="override the target value in seconds (default from profile)",
    )
    ap.add_argument("--out", help="write the patched module here")
    ap.add_argument("--check", action="store_true", help="check stock only")
    ap.add_argument("--json", help="write a JSON report")
    args = ap.parse_args(argv)

    doc, off, count, stride, expected = load_profile(args.profile)
    module = Path(args.module).read_bytes()
    end = off + count * stride
    if off < 0 or end > len(module):
        raise SystemExit("table 0x%X..0x%X is outside the module" % (off, end))

    stock = [u32(module, off + i * stride) for i in range(count)]
    mismatches = [
        (i, stock[i], expected[i]) for i in range(count) if stock[i] != expected[i]
    ]
    if mismatches:
        print("stock check FAILED (%d/%d entries differ):" % (len(mismatches), count))
        for i, got, want in mismatches[:20]:
            print(
                "  entry %2d @0x%X: got %d, expected %d"
                % (i, off + i * stride, got, want)
            )
        return 2

    marker = doc.get("end_marker")
    if marker is not None and u32(module, end) != int(marker):
        print(
            "end-marker check FAILED: 0x%X = %d, expected %d"
            % (end, u32(module, end), int(marker))
        )
        return 2

    target_seconds = args.seconds
    if target_seconds is None:
        target_seconds = int(doc["target_seconds"])
    target_ms = target_seconds * 1000
    if not (1 <= target_ms < 2**32):
        raise SystemExit("target value out of u32 range: %d" % target_ms)

    print("model   : %s" % doc.get("model", "?"))
    print("module  : %s (%d bytes, sha256 %s)" % (args.module, len(module), sha256(module)))
    print("table   : 0x%X, %d entries, stride %d" % (off, count, stride))
    print("target  : %s" % fmt_ms(target_ms))
    print()
    print("  idx  offset      stock        new")
    for i in range(count):
        print(
            "  %3d  0x%08X  %-12d %-12d"
            % (i, off + i * stride, stock[i], target_ms)
        )
    print()
    print("stock check OK (%d entries match)" % count)

    report = {
        "model": doc.get("model"),
        "firmware": doc.get("firmware"),
        "module": args.module,
        "module_sha256_stock": sha256(module),
        "table": {"offset": "0x%X" % off, "count": count, "stride": stride},
        "target_seconds": target_seconds,
        "target_ms": target_ms,
        "entries": [
            {
                "index": i,
                "offset": "0x%X" % (off + i * stride),
                "stock_ms": stock[i],
                "new_ms": target_ms,
            }
            for i in range(count)
        ],
    }

    if args.check:
        print("check only: no file written")
        if args.json:
            Path(args.json).write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        return 0

    if not args.out:
        raise SystemExit("nothing to do: pass --out or --check")

    patched = bytearray(module)
    for i in range(count):
        struct.pack_into("<I", patched, off + i * stride, target_ms)

    diff = [i for i in range(len(module)) if module[i] != patched[i]]
    allowed = set(range(off, end))
    outside = [i for i in diff if i not in allowed]
    if outside:
        raise SystemExit(
            "internal error: %d changed bytes outside the table (first 0x%X)"
            % (len(outside), outside[0])
        )

    Path(args.out).write_bytes(patched)
    report["module_sha256_patched"] = sha256(patched)
    report["changed_bytes"] = len(diff)
    report["changed_range"] = "0x%X..0x%X" % (min(diff), max(diff) + 1)
    report["outside_table"] = 0

    print()
    print("wrote %s" % args.out)
    print("changed bytes: %d, range 0x%X..0x%X, outside table: 0"
          % (len(diff), min(diff), max(diff) + 1))
    print("sha256: %s" % report["module_sha256_patched"])
    if args.json:
        Path(args.json).write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("report: %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
