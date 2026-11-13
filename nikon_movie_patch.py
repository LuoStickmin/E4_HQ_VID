#!/usr/bin/env python3
"""Configurable Nikon DSLR movie-mode table / menu-label patcher.

The tool is deliberately data-driven: a profile (built-in or a JSON file)
describes where the movie-mode table lives, which entries to change, and which
UTF-16 menu labels to replace.  Every edit is checked against the expected
stock value first, and the final module is verified so that no byte outside the
declared fields changes.

Current built-in profile:
    d7200-hq64   D7200 C 1.04, 1080p60 HQ 42/35 -> 64/60 Mbps,
                 menu label "1080 60p Hq" (lowercase q: the menu font has no
                 uppercase Q glyph).

Usage:
    python nikon_movie_patch.py --module b1230_104.bin --profile d7200-hq64 --check
    python nikon_movie_patch.py --module b1230_104.bin --profile d7200-hq64 \
        --out b1230_104.hq64.bin --json report.json

    # arbitrary profile
    python nikon_movie_patch.py --module b1230_104.bin --config my.json --out ...

Config schema (JSON):
{
  "name": "d7200-hq64",
  "model": "D7200",
  "table": {
    "offset": 0x2ACD8C,
    "stride": 28,
    "count": 22,
    "fields": {"wh": 0, "tb_num": 4, "tb_den": 8, "fps": 12,
               "rate_a": 16, "rate_b": 20, "flag": 24}
  },
  "patches": [
    {"type": "movie_rate", "entry": 1, "rates": [64000000, 60000000],
     "expect": {"width": 1920, "height": 1080,
                "tb_num": 60000, "tb_den": 1001,
                "rates": [42000000, 35000000], "flag": 1}},
    {"type": "utf16_label", "offset": 0x59B05C,
     "expect": "1920x1080; 60p", "value": "1080 60p Hq   "},
    {"type": "utf16_label", "offset": 0x6C9192,
     "expect": "1920x1080;60p", "value": "1080 60p Hq  "}
  ]
}
"""

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

DEFAULT_FIELDS = {
    "wh": 0,
    "tb_num": 4,
    "tb_den": 8,
    "fps": 12,
    "rate_a": 16,
    "rate_b": 20,
    "flag": 24,
}

PROFILES = {
    "d7200-hq64": {
        "name": "d7200-hq64",
        "model": "D7200",
        "table": {
            "offset": 0x2ACD8C,
            "stride": 0x1C,
            "count": 22,
            "fields": DEFAULT_FIELDS,
        },
        "patches": [
            {
                "type": "movie_rate",
                "entry": 1,
                "rates": [64_000_000, 60_000_000],
                "expect": {
                    "width": 1920,
                    "height": 1080,
                    "tb_num": 60000,
                    "tb_den": 1001,
                    "rates": [42_000_000, 35_000_000],
                    "flag": 1,
                },
            },
            {
                "type": "utf16_label",
                "offset": 0x59B05C,
                "expect": "1920x1080; 60p",
                "value": "1080 60p Hq   ",
            },
            {
                "type": "utf16_label",
                "offset": 0x6C9192,
                "expect": "1920x1080;60p",
                "value": "1080 60p Hq  ",
            },
        ],
    },
}


def as_int(value, what):
    if isinstance(value, int):
        return value
    try:
        return int(str(value), 0)
    except (TypeError, ValueError):
        raise ValueError("%s is not an integer: %r" % (what, value))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def utf16(data, off, chars):
    return data[off:off + chars * 2].decode("utf-16le")


def read_record(data, table, index):
    off = as_int(table["offset"], "table.offset") + index * as_int(table["stride"], "table.stride")
    fields = {k: as_int(v, "table.fields." + k)
              for k, v in table.get("fields", DEFAULT_FIELDS).items()}
    need = max(fields.values()) + 4
    if off + need > len(data):
        raise ValueError("entry %d is outside the module" % (index + 1))
    wh = struct.unpack_from("<I", data, off + fields["wh"])[0]
    return {
        "offset": off,
        "width": wh & 0xFFFF,
        "height": wh >> 16,
        "tb_num": struct.unpack_from("<I", data, off + fields["tb_num"])[0],
        "tb_den": struct.unpack_from("<I", data, off + fields["tb_den"])[0],
        "fps": struct.unpack_from("<I", data, off + fields["fps"])[0],
        "rate_a": struct.unpack_from("<I", data, off + fields["rate_a"])[0],
        "rate_b": struct.unpack_from("<I", data, off + fields["rate_b"])[0],
        "flag": struct.unpack_from("<I", data, off + fields["flag"])[0],
    }


def check_patch(data, patch):
    kind = patch["type"]
    if kind == "movie_rate":
        table = patch["_table"]
        entry = as_int(patch["entry"], "entry") - 1
        rec = read_record(data, table, entry)
        exp = patch.get("expect", {})
        for key in ("width", "height", "tb_num", "tb_den", "fps", "flag"):
            if key in exp and rec[key] != as_int(exp[key], "expect." + key):
                raise ValueError(
                    "entry %d %s: stock %r, expected %r"
                    % (entry + 1, key, rec[key], as_int(exp[key], "expect." + key))
                )
        if "rates" in exp:
            want = tuple(as_int(x, "expect.rates") for x in exp["rates"])
            if (rec["rate_a"], rec["rate_b"]) != want:
                raise ValueError(
                    "entry %d rates: stock %r, expected %r"
                    % (entry + 1, (rec["rate_a"], rec["rate_b"]), want)
                )
        rates = tuple(as_int(x, "rates") for x in patch["rates"])
        if len(rates) != 2 or rates[0] <= 0 or rates[1] <= 0:
            raise ValueError("rates must be two positive integers")
        return rec, rates
    if kind == "utf16_label":
        off = as_int(patch["offset"], "offset")
        expect = patch["expect"]
        value = patch["value"]
        if len(expect) != len(value):
            raise ValueError(
                "label at 0x%X: replacement length %d != stock length %d "
                "(packed UTF-16 pool requires equal length)"
                % (off, len(value), len(expect))
            )
        got = utf16(data, off, len(expect))
        if got != expect:
            raise ValueError("label at 0x%X: stock %r, expected %r"
                             % (off, got, expect))
        return off, value
    if kind == "raw_bytes":
        off = as_int(patch["offset"], "offset")
        old = bytes.fromhex(patch["expect_hex"])
        new = bytes.fromhex(patch["value_hex"])
        if len(old) != len(new):
            raise ValueError("raw_bytes at 0x%X: length changed" % off)
        if data[off:off + len(old)] != old:
            raise ValueError("raw_bytes at 0x%X: stock %s, expected %s"
                             % (off, data[off:off + len(old)].hex(), old.hex()))
        return off, new
    raise ValueError("unknown patch type: %r" % kind)


def apply_profile(data, profile):
    table = profile["table"]
    patches = profile["patches"]
    out = bytearray(data)
    changes = []
    ranges = []
    for patch in patches:
        patch = dict(patch)
        patch["_table"] = table
        kind = patch["type"]
        if kind == "movie_rate":
            rec, rates = check_patch(data, patch)
            fields = {k: as_int(v, "table.fields." + k)
                      for k, v in table.get("fields", DEFAULT_FIELDS).items()}
            off_a = rec["offset"] + fields["rate_a"]
            off_b = rec["offset"] + fields["rate_b"]
            struct.pack_into("<II", out, off_a, rates[0], rates[1])
            changes.append({
                "type": kind,
                "entry": rec["offset"],
                "offset_rate_a": off_a,
                "offset_rate_b": off_b,
                "old": [rec["rate_a"], rec["rate_b"]],
                "new": list(rates),
            })
            ranges.append((off_a, off_a + 4))
            ranges.append((off_b, off_b + 4))
        elif kind == "utf16_label":
            off, value = check_patch(data, patch)
            raw = value.encode("utf-16le")
            out[off:off + len(raw)] = raw
            changes.append({
                "type": kind,
                "offset": off,
                "old": patch["expect"],
                "new": value,
            })
            ranges.append((off, off + len(raw)))
        elif kind == "raw_bytes":
            off, new = check_patch(data, patch)
            out[off:off + len(new)] = new
            changes.append({
                "type": kind,
                "offset": off,
                "old_hex": patch["expect_hex"],
                "new_hex": patch["value_hex"],
            })
            ranges.append((off, off + len(new)))
    return bytes(out), changes, ranges


def verify_scope(original, patched, ranges):
    if len(original) != len(patched):
        raise ValueError("module size changed")
    allowed = set()
    for lo, hi in ranges:
        allowed.update(range(lo, hi))
    diffs = {i for i, (a, b) in enumerate(zip(original, patched)) if a != b}
    if not diffs <= allowed:
        raise ValueError("diff outside declared fields: %s"
                         % sorted(diffs - allowed)[:20])
    return len(diffs)


def load_profile(args):
    if args.profile:
        if args.profile not in PROFILES:
            raise SystemExit("unknown profile %r (built-in: %s)"
                             % (args.profile, ", ".join(sorted(PROFILES))))
        return PROFILES[args.profile]
    if args.config:
        return json.loads(Path(args.config).read_text(encoding="utf-8"))
    raise SystemExit("one of --profile/--config is required")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--module", required=True, help="decrypted main module")
    ap.add_argument("--profile", choices=sorted(PROFILES),
                    help="built-in profile")
    ap.add_argument("--config", help="external JSON profile")
    ap.add_argument("--out", help="patched module to write")
    ap.add_argument("--json", help="write a JSON report here")
    ap.add_argument("--check", action="store_true",
                    help="validate stock values without writing")
    args = ap.parse_args(argv)

    profile = load_profile(args)
    data = Path(args.module).read_bytes()
    try:
        patched, changes, ranges = apply_profile(data, profile)
        changed = verify_scope(data, patched, ranges)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    print("profile  %s (%s)" % (profile.get("name", "custom"),
                                profile.get("model", "?")))
    print("module   %s" % args.module)
    for c in changes:
        if c["type"] == "movie_rate":
            print("  entry @0x%06X  rate %s -> %s"
                  % (c["entry"], c["old"], c["new"]))
        elif c["type"] == "utf16_label":
            print("  label @0x%06X  %r -> %r"
                  % (c["offset"], c["old"], c["new"]))
        else:
            print("  raw   @0x%06X  %s -> %s"
                  % (c["offset"], c["old_hex"], c["new_hex"]))
    print("changed bytes: %d" % changed)

    if args.check:
        print("stock checks passed; nothing written")
        return 0
    if not args.out:
        ap.error("--out is required unless --check is used")
    if Path(args.out).resolve() == Path(args.module).resolve():
        print("error: --out must not be the stock module", file=sys.stderr)
        return 2

    Path(args.out).write_bytes(patched)
    doc = {
        "profile": profile.get("name", "custom"),
        "model": profile.get("model", "?"),
        "module": {
            "size": len(data),
            "sha256_stock": sha256(data),
            "sha256_patched": sha256(patched),
            "changed_bytes": changed,
        },
        "changes": changes,
        "repack_hint": (
            "python repack_firmware.py --key key_all.json "
            "--firmware <stock image> --replace-module %s=%s "
            "--keep-tags --out <patched image>"
            % (Path(args.module).name, args.out)
        ),
    }
    if args.json:
        Path(args.json).write_text(
            json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print("patched  %s  %s" % (args.out, doc["module"]["sha256_patched"]))
    print("repack:  %s" % doc["repack_hint"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
