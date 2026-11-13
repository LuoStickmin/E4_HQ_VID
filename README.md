# E4_HQ_VID

EXPEED 4 DSLR movie bitrate / menu-label patcher.

The goal is a **data-driven, multi-model** workflow:

- patch the movie-mode table (bitrate fields) instead of hard-coded byte edits;
- replace UTF-16 menu labels in place (same length, no pool reflow);
- verify every stock value before writing;
- verify the final module differs only in the declared fields;
- repack the firmware with the new checksum/encryption toolchain.

## Supported models

| Model | Firmware | Profile | Status |
| --- | --- | --- | --- |
| D7200 | C 1.04 (`D7200_0104`) | `profiles/d7200_hq64.json` | stock-checked; current 1080p60 HQ 64/60 Mbps + `Hq` label; camera-tested by the author |
| D750 | 1.15 (`D750_0115`) | `profiles/d750_hq64.json` | stock-checked; not camera-tested |
| D810 | 1.14 (`D810_0114`) | `profiles/d810_hq64.json` | stock-checked; not camera-tested |
| D3400 | C 1.13 (`D3400_0113`) | `profiles/d3400_hq64.json` | stock-checked; **packaging B** (header digest / K8 unknown), module patch works, full repack needs K8 or `--allow-stale-header`; not camera-tested |

D3400 uses the combined "Movie frame size/quality" labels, so its profile
patches both the 1080p60 frame-size label and the
`1920x1080; 60p; high quality` combined label.

A profile only encodes *where* the table and labels are.  If you have a
decrypted module for another EXPEED 4 body, `scan_movie_modes.py` can emit a
profile skeleton and you can add it without touching the patcher.

## Quick start

```bash
pip install -r requirements.txt
```

The tools do not ship firmware or keys.  Put your own `key_all.json` in
`keys/` (git-ignored) or pass `--key`.

### 1. Decrypt a firmware image

```bash
python tools/decrypt_dslr2.py --key keys/key_all.json \
  --firmware D750_0115.bin --out D750_0115.dec
```

This creates `D750_0115.dec.modules/`.  The main module is the large
`b*.bin` file (D750: `b1010_115a.bin`; D7200: `b1230_104.bin`; D810:
`b920_114.bin`).

### 2. Check a profile against stock

```bash
python nikon_movie_patch.py \
  --module D750_0115.dec.modules/b1010_115a.bin \
  --config profiles/d750_hq64.json --check
```

### 3. Write the patched module

```bash
python nikon_movie_patch.py \
  --module D750_0115.dec.modules/b1010_115a.bin \
  --config profiles/d750_hq64.json \
  --out D750_0115.dec.modules/b1010_115a.hq64.bin \
  --json hq64.json
```

### 4. Repack

```bash
python tools/repack_firmware.py --key keys/key_all.json \
  --firmware D750_0115.bin \
  --replace-module b1010_115a.bin=D750_0115.dec.modules/b1010_115a.hq64.bin \
  --keep-tags --out D750_0115.hq64.bin
```

`repack_firmware.py` refuses to write a packaging-B image with a stale header
digest (D850/D5 class) unless `--allow-stale-header` is passed.  The current
profiles are packaging A (no header digest), so this does not apply.

## What the profiles change

Current D7200 profile (`d7200_hq64.json`):

- table `0x2ACD8C`, entry 1 (1-based) = 1920×1080 60p HQ;
- `rate_a/rate_b`: 42/35 → **64/60 Mbps**;
- English label `0x59B05C`: `1920x1080; 60p` → `1080 60p Hq`;
- Chinese label `0x6C9192`: `1920x1080;60p` → `1080 60p Hq`.

D750 and D810 profiles do the same for their 1080p60 HQ entry.

The label replacement is deliberately **same-length**: the menu labels live in
a packed UTF-16 pool, and a longer string would shift every following label.
That is also why the short `1080 60p Hq` form is used instead of
`1920x1080; 60p HQ`.

## Add a new model

```bash
python scan_movie_modes.py --module path/to/b1234_100.bin --model D3500 \
  --emit-profile profiles/d3500_hq64.json
```

Then review the emitted profile:

1. the scanner ranks candidate tables; confirm the base and the first entry
   (resolution/timebase/rates/flag);
2. confirm the EN/ZH `1920x1080; 60p` label offsets and lengths;
3. set the target rates (default 64/60 Mbps);
4. run `nikon_movie_patch.py --check` before writing;
5. repack and verify by decrypting the output and comparing modules.

See [docs/ADD_MODEL.md](docs/ADD_MODEL.md) for the schema and the pitfalls.

## Repository layout

```
nikon_movie_patch.py      data-driven patcher
scan_movie_modes.py       read-only table/label scanner
profiles/                 per-model JSON profiles
tools/                    decrypt + repack toolchain
tests/                    profile/patcher tests
docs/                     usage and add-model notes
keys/                     put key_all.json here (git-ignored)
```

## Boundaries

- No firmware, keys, decrypted modules, or flashable images are included.
- Stock checks and container CRC checks prove the image is self-consistent, not
  that the camera accepts it.
- Camera testing is the only proof of behavior; keep the stock update file for
  recovery.
- Firmware copyright belongs to Nikon.  Use only on hardware you own.
