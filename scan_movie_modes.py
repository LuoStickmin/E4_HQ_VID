#!/usr/bin/env python3
"""Read-only scanner for Nikon movie-mode tables and UTF-16 menu labels.

The scanner is meant for bringing up a new model (for example D3400) without
guessing offsets.  It looks for:

1. candidate 22-entry movie tables with 0x1C stride, anchored on 1920x1080,
   1280x720 and 640x424 packed width/height words;
2. UTF-16 menu labels "Frame size/frame rate", "Movie quality",
   "1920x1080; 60p" / "1920x1080;60p".

It never writes to the module.  With --emit-profile it writes a JSON profile
skeleton that can be reviewed and filled in.

Usage:
    python scan_movie_modes.py --module b1230_104.bin
    python scan_movie_modes.py --module b1230_104.bin --model D7200 --emit-profile profiles/d7200.json
"""

import argparse
import json
import struct
import sys
from pathlib import Path

DEFAULT_OFFSETS = {"wh": 0, "tb_num": 4, "tb_den": 8, "fps": 12,
                   "rate_a": 16, "rate_b": 20, "flag": 24}
KNOWN_SIZES = {(1920, 1080), (1280, 720), (640, 424), (640, 480),
               (320, 240), (3840, 2160)}


def u32(data, off):
    return struct.unpack_from("<I", data, off)[0]


def decode_entry(data, off, fields):
    wh = u32(data, off + fields["wh"])
    return {
        "offset": off,
        "width": wh & 0xFFFF,
        "height": wh >> 16,
        "tb_num": u32(data, off + fields["tb_num"]),
        "tb_den": u32(data, off + fields["tb_den"]),
        "fps": u32(data, off + fields["fps"]),
        "rate_a": u32(data, off + fields["rate_a"]),
        "rate_b": u32(data, off + fields["rate_b"]),
        "flag": u32(data, off + fields["flag"]),
    }


def entry_score(e):
    w, h = e["width"], e["height"]
    if not (160 <= w <= 8192 and 90 <= h <= 4320):
        return 0
    if not (1000 <= e["tb_num"] <= 120000 and 1 <= e["tb_den"] <= 2000):
        return 0
    if not (1 <= e["fps"] <= 240):
        return 0
    if not (0 <= e["rate_a"] <= 200_000_000 and 0 <= e["rate_b"] <= 200_000_000):
        return 0
    if e["flag"] not in (0, 1):
        return 0
    score = 1
    if (w, h) in KNOWN_SIZES:
        score += 2
    if e["rate_a"] > 1_000_000:
        score += 1
    if e["tb_num"] / e["tb_den"] >= 10:
        score += 1
    return score


def find_tables(data, stride=0x1C, count=22, fields=None):
    fields = fields or DEFAULT_OFFSETS
    anchors = []
    for size in ((1920, 1080), (1280, 720), (640, 424)):
        wh = (size[1] << 16) | size[0]
        pat = struct.pack("<I", wh)
        start = 0
        while True:
            pos = data.find(pat, start)
            if pos < 0:
                break
            anchors.append(pos)
            start = pos + 1
    bases = set()
    for pos in anchors:
        for i in range(count):
            base = pos - i * stride
            if base >= 0 and base + count * stride <= len(data):
                bases.add(base)
    candidates = []
    for base in sorted(bases):
        entries = [decode_entry(data, base + i * stride, fields)
                   for i in range(count)]
        scores = [entry_score(e) for e in entries]
        good = sum(1 for s in scores if s > 0)
        total = sum(scores)
        sizes = {(e["width"], e["height"]) for e in entries}
        if good >= count - 2 and total >= count * 2:
            candidates.append({
                "base": base,
                "good": good,
                "score": total,
                "sizes": sorted(sizes),
                "entries": entries,
            })
    candidates.sort(key=lambda c: (-c["score"], c["base"]))
    return candidates


def find_utf16(data, text):
    needle = text.encode("utf-16le")
    out = []
    start = 0
    while True:
        pos = data.find(needle, start)
        if pos < 0:
            break
        out.append(pos)
        start = pos + 1
    return out


def context(data, off, chars=48):
    raw = data[off:off + chars * 2]
    return raw.decode("utf-16le", "replace")


def same_length_value(expect, base="1080 60p Hq"):
    if len(base) > len(expect):
        base = base[:len(expect)]
    return base + " " * (len(expect) - len(base))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--module", required=True)
    ap.add_argument("--model", default="UNKNOWN")
    ap.add_argument("--stride", type=lambda x: int(x, 0), default=0x1C)
    ap.add_argument("--count", type=int, default=22)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--emit-profile", help="write a profile skeleton JSON")
    ap.add_argument("--json", help="write scan results as JSON")
    args = ap.parse_args(argv)

    data = Path(args.module).read_bytes()
    print("module %s (%d bytes)" % (args.module, len(data)))
    tables = find_tables(data, args.stride, args.count)
    print("\n-- movie-table candidates")
    if not tables:
        print("  none")
    for n, cand in enumerate(tables[:args.top], 1):
        print("  #%d base 0x%X score=%d sizes=%s"
              % (n, cand["base"], cand["score"],
                 ", ".join("%dx%d" % s for s in cand["sizes"])))
        for e in cand["entries"][:6]:
            print("     %4dx%-4d tb=%d/%d fps=%d rate=%d/%d flag=%d"
                  % (e["width"], e["height"], e["tb_num"], e["tb_den"],
                     e["fps"], e["rate_a"], e["rate_b"], e["flag"]))

    print("\n-- UTF-16 anchors")
    anchors = {}
    for text in ("Frame size/frame rate", "Movie quality",
                 "1920x1080; 60p", "1920x1080;60p", "1920x1080 60p"):
        offs = find_utf16(data, text)
        anchors[text] = offs
        print("  %-24r %d %s" % (text, len(offs),
                                 [hex(x) for x in offs[:8]]))
        for off in offs[:2]:
            print("      %s" % context(data, off, 40).replace("\n", "\\n"))

    if args.json:
        doc = {"module": args.module, "model": args.model,
               "tables": tables[:args.top], "anchors": anchors}
        Path(args.json).write_text(json.dumps(doc, indent=2, ensure_ascii=False)
                                   + "\n", encoding="utf-8")

    if args.emit_profile:
        if not tables:
            print("error: no table candidate; cannot emit profile", file=sys.stderr)
            return 2
        best = tables[0]
        entries = best["entries"]
        en = (anchors.get("1920x1080; 60p") or [None])[0]
        zh = (anchors.get("1920x1080;60p") or [None])[0]
        profile = {
            "name": args.model.lower() + "-hq64",
            "model": args.model,
            "table": {
                "offset": "0x%X" % best["base"],
                "stride": args.stride,
                "count": args.count,
                "fields": DEFAULT_OFFSETS,
            },
            "patches": [
                {
                    "type": "movie_rate",
                    "entry": 1,
                    "rates": [64000000, 60000000],
                    "expect": {
                        "width": entries[0]["width"],
                        "height": entries[0]["height"],
                        "tb_num": entries[0]["tb_num"],
                        "tb_den": entries[0]["tb_den"],
                        "rates": [entries[0]["rate_a"], entries[0]["rate_b"]],
                        "flag": entries[0]["flag"],
                    },
                }
            ],
            "notes": [
                "Review the table base and first entry; the scanner may pick a "
                "sibling table.",
                "Add utf16_label patches after confirming the menu label offsets.",
            ],
        }
        if en is not None:
            expect = context(data, en, 14)[:14]
            profile["patches"].append({
                "type": "utf16_label", "offset": "0x%X" % en,
                "expect": expect, "value": same_length_value(expect),
            })
        if zh is not None:
            expect = context(data, zh, 13)[:13]
            profile["patches"].append({
                "type": "utf16_label", "offset": "0x%X" % zh,
                "expect": expect, "value": same_length_value(expect),
            })
        Path(args.emit_profile).write_text(
            json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print("\nwrote profile skeleton %s" % args.emit_profile)
    return 0


if __name__ == "__main__":
    sys.exit(main())
