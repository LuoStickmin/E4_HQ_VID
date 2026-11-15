# Usage

## Prerequisites

- Python 3.9+
- NumPy (`pip install -r requirements.txt`) for `tools/decrypt_firmware.py`
- A local, legally obtained firmware image
- A `key_all.json` covering that model/firmware (not included)

## 1. Decrypt and carve

```bash
python tools/decrypt_dslr2.py --key keys/key_all.json \
  --firmware D750_0115.bin --out D750_0115.dec
```

Output layout:

```
D750_0115.dec
D750_0115.dec.modules/
  a1010_011100.bin
  b1010_115a.bin     <- main module, use this
  _wma_ver01.00.00
```

The main module is the large `b*.bin` (D7200: `b1230_104.bin`, D750:
`b1010_115a.bin`, D810: `b920_114.bin`, D3400: `b1480_113.bin`).

## 2. Check stock

```bash
python nikon_movie_patch.py \
  --module D750_0115.dec.modules/b1010_115a.bin \
  --config profiles/d750_hq64.json --check
```

The patcher checks every expected field and label, then prints the planned
changes and the changed-byte count.  It writes nothing.

## 3. Write the patched module

```bash
python nikon_movie_patch.py \
  --module D750_0115.dec.modules/b1010_115a.bin \
  --config profiles/d750_hq64.json \
  --out D750_0115.dec.modules/b1010_115a.hq64.bin \
  --json hq64.json
```

The output is verified so that no byte outside the declared rate fields and
label ranges changed.

## 4. Repack

```bash
python tools/repack_firmware.py --key keys/key_all.json \
  --firmware D750_0115.bin \
  --replace-module b1010_115a.bin=D750_0115.dec.modules/b1010_115a.hq64.bin \
  --keep-tags --out D750_0115.hq64.bin
```

The new `repack_firmware.py`:

- rebuilds the directory and both CRC levels;
- re-encrypts when the input was encrypted;
- validates the output with `decrypt_firmware.validate_firmware()`;
- refuses a stale packaging-B header digest unless `--k8` (recompute) or
  `--allow-stale-header` (test only) is given.  D7200/D750/D810 are packaging A,
  so this does not affect them.

**D3400 is packaging B.**  Its 32-byte header contains `SHA1(body || K8)`.
D3400's K8 was recovered on 2026-11-15 as `AF08FBDBB582B587`; pass it to
`repack_firmware.py` as a JSON file:

```json
{"K8": "AF08FBDBB582B587", "self_check": "749237c5e12cfbf8d70e34ef363d9de3e243a6bb81cc9d6b7ab3d29a00580cac"}
```

```bash
python tools/repack_firmware.py --key keys/key_all.json \
  --firmware D3400_0113.bin \
  --replace-module b1480_113.bin=D3400_0113.dec.modules/b1480_113.hq64.bin \
  --k8 keys/d3400_0113_k8.json --keep-tags --out D3400_0113.hq64.bin
```

The tool verifies the stock digest before writing and recomputes it for the new
body.  Without `--k8` it still refuses the image by default.  A matching digest
does not prove the camera accepts the image; `--allow-stale-header` remains a
test-only escape hatch.

D3400 also uses the combined "Movie frame size/quality" labels, so
`profiles/d3400_hq64.json` patches both the separate 1080p60 frame-size label and
the `1920x1080; 60p; high quality` combined label (English and Chinese).

## 5. Verify

Decrypt the output and compare the modules:

```bash
python tools/decrypt_dslr2.py --key keys/key_all.json \
  --firmware D750_0115.hq64.bin --out D750_0115.hq64.dec
```

- the edited module should equal the patched module;
- the other modules should be byte-identical to stock;
- the diff should be only the rate fields and labels.

## Profile schema

```json
{
  "name": "d750-hq64",
  "model": "D750",
  "table": {
    "offset": "0x2AA99C",
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
    {"type": "utf16_label", "offset": "0x754A96",
     "expect": "1920x1080; 60p", "value": "1080 60p Hq   "},
    {"type": "utf16_label", "offset": "0x885E12",
     "expect": "1920x1080;60p", "value": "1080 60p Hq  "}
  ]
}
```

- `entry` is 1-based.
- `rates` are `rate_a`/`rate_b` in bps.
- `expect` must match stock exactly.
- `utf16_label` replacement must have the same number of UTF-16 code units as
  the stock string.  Trailing spaces are used to pad.
- `raw_bytes` is available for arbitrary patches:
  `{"type":"raw_bytes","offset":"0x...","expect_hex":"...","value_hex":"..."}`.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `label ... replacement length ... != stock length` | packed UTF-16 pool; use a same-length label or a shorter compact form |
| `entry ... rates: stock ..., expected ...` | wrong firmware revision or wrong table offset |
| `diff outside declared fields` | profile points at the wrong field; do not flash |
| `stale packaging-B header digest` | wrapper B (e.g. D3400); pass `--k8 <json>` to verify/recompute, or `--allow-stale-header` for CRC/QEMU tests only. This repo ships no K8 files; D3400's is `AF08FBDBB582B587` |
| menu shows a placeholder glyph | camera font lacks that character; use a character present in stock labels (e.g. lowercase `q` instead of uppercase `Q`) |
