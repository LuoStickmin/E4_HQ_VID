# Adding a model (D3400 and others)

The patcher is model-agnostic; a model is just a JSON profile.  The scanner
finds the two things a profile needs: the movie-mode table and the UTF-16 menu
labels.

## 1. Get a decrypted main module

Decrypt the update image with `tools/decrypt_dslr2.py`, then pick the large
`b*.bin` from `*.dec.modules/`:

| Model | Main module (typical) |
| --- | --- |
| D7200 | `b1230_104.bin` |
| D750 | `b1010_115a.bin` |
| D810 | `b920_114.bin` |
| D3400 | `b1xxx_yyy.bin` (check the decrypted directory) |

## 2. Run the scanner

```bash
python scan_movie_modes.py --module b1xxx_yyy.bin --model D3400
```

It prints:

- ranked movie-table candidates with base offset, size set, and first entries;
- UTF-16 offsets for `Frame size/frame rate`, `Movie quality`,
  `1920x1080; 60p` and `1920x1080;60p`.

For D7200/D750/D810 the top candidate is the real table; the runner-up is
usually the same table shifted by one entry.  Confirm by checking that the
first entry is `1920x1080`, `60000/1001`, `42000000/35000000`, flag `1`, and
that the 22 entries include 720p and 640×424.

## 3. Emit a skeleton

```bash
python scan_movie_modes.py --module b1xxx_yyy.bin --model D3400 \
  --emit-profile profiles/d3400_hq64.json
```

Review the output before using it:

- `table.offset` must be the candidate whose entry 1 matches the stock
  1080p60 HQ row;
- `table.fields` is the shared 0x1C-byte layout
  (`wh, tb_num, tb_den, fps, rate_a, rate_b, flag`);
- the scanner picks the first `1920x1080; 60p` (English) and
  `1920x1080;60p` (Chinese) anchors.  Confirm they are the menu labels, not a
  help string: the context should be followed by `1920x1080; 50p` and then
  `Destination`/`目标位置`.

## 4. Fill the profile

```json
{
  "name": "d3400-hq64",
  "model": "D3400",
  "table": {"offset": "0x...", "stride": 28, "count": 22,
            "fields": {"wh": 0, "tb_num": 4, "tb_den": 8, "fps": 12,
                       "rate_a": 16, "rate_b": 20, "flag": 24}},
  "patches": [
    {"type": "movie_rate", "entry": 1, "rates": [64000000, 60000000],
     "expect": {"width": 1920, "height": 1080,
                "tb_num": 60000, "tb_den": 1001,
                "rates": [42000000, 35000000], "flag": 1}},
    {"type": "utf16_label", "offset": "0x...",
     "expect": "1920x1080; 60p", "value": "1080 60p Hq   "},
    {"type": "utf16_label", "offset": "0x...",
     "expect": "1920x1080;60p", "value": "1080 60p Hq  "}
  ]
}
```

Rules:

- `entry` is 1-based; entry 1 is the 1080p60 HQ row.
- `rates` are bps; 64/60 Mbps = 64000000/60000000.
- `expect` must match the stock module exactly.
- `utf16_label` replacement must be the **same number of UTF-16 code units** as
  `expect`; pad with spaces.  A longer string would shift the packed language
  pool.
- If the menu font lacks a character, use one that exists in stock labels.
  On D7200, uppercase `Q` rendered as a placeholder; lowercase `q` works
  (`Hq`).

## 5. Check, patch, repack

```bash
python nikon_movie_patch.py --module b1xxx_yyy.bin \
  --config profiles/d3400_hq64.json --check

python nikon_movie_patch.py --module b1xxx_yyy.bin \
  --config profiles/d3400_hq64.json \
  --out b1xxx_yyy.hq64.bin --json d3400_hq64.json
```

Then repack with `tools/repack_firmware.py` and verify by decrypting the output.

## 6. What the scanner cannot decide

- Whether the camera accepts the image.
- Whether 64 Mbps is within the encoder/thermal/card limits for that body.
- Whether the menu font has the glyphs you choose.
- Whether the model's wrapper is packaging A or B (check `repack_firmware.py`
  output; packaging B needs K8 or a stale-header decision).

Always keep the stock update file for recovery.
