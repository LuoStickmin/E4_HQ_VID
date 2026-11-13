# E4_HQ_VID

[中文](README.md) | [English](README.en.md)

> ## ⚠️ Disclaimer
>
> - This project is **not affiliated with, authorized by, or endorsed by Nikon**.
>   Nikon, EXPEED and related marks belong to their respective owners.
> - This repository contains **no firmware, decrypted modules, keys, or flashable
>   images**. You must obtain the firmware and `key_all.json` legally yourself.
> - Modifying, repacking or flashing firmware can brick a camera, void the
>   warranty, destroy data, or violate local law. **You do this at your own risk.**
> - The project is intended for research, interoperability and format analysis on
>   hardware you own. It is not intended to circumvent copyright protection or
>   technological protection measures. Use it only where your jurisdiction allows.
> - The authors and contributors accept no liability for direct or indirect loss.
>   Keep the stock firmware and a recovery path before flashing.
>
> See [LEGAL.md](LEGAL.md) for the full terms. By using this repository you agree
> to them.

## Reproduce the current D7200 C 1.04 state

Goal: 1080p60 **HQ** `42/35 → 64/60 Mbps`, menu label `1080 60p Hq`.

You need `D7200_0104.bin` (stock C 1.04) and a `key_all.json` that covers it.

### Windows PowerShell

```powershell
git clone https://github.com/LuoStickmin/E4_HQ_VID.git
cd E4_HQ_VID
python -m pip install -r requirements.txt
mkdir keys
copy C:\path\to\key_all.json keys\key_all.json

# 1. decrypt
python tools\decrypt_dslr2.py --key keys\key_all.json `
  --firmware C:\path\to\D7200_0104.bin `
  --out C:\path\to\D7200_0104.dec

# 2. stock check only
python nikon_movie_patch.py `
  --module C:\path\to\D7200_0104.dec.modules\b1230_104.bin `
  --config profiles\d7200_hq64.json --check

# 3. write the patched module
python nikon_movie_patch.py `
  --module C:\path\to\D7200_0104.dec.modules\b1230_104.bin `
  --config profiles\d7200_hq64.json `
  --out C:\path\to\D7200_0104.dec.modules\b1230_104.hq64.bin `
  --json C:\path\to\hq64.json

# 4. repack
python tools\repack_firmware.py --key keys\key_all.json `
  --firmware C:\path\to\D7200_0104.bin `
  --replace-module b1230_104.bin=C:\path\to\D7200_0104.dec.modules\b1230_104.hq64.bin `
  --keep-tags --out C:\path\to\D7200_0104.hq64.bin
```

### Linux / macOS

```bash
git clone https://github.com/LuoStickmin/E4_HQ_VID.git
cd E4_HQ_VID
python3 -m pip install -r requirements.txt
mkdir -p keys
cp /path/to/key_all.json keys/key_all.json

python3 tools/decrypt_dslr2.py --key keys/key_all.json \
  --firmware /path/to/D7200_0104.bin --out /path/to/D7200_0104.dec

python3 nikon_movie_patch.py \
  --module /path/to/D7200_0104.dec.modules/b1230_104.bin \
  --config profiles/d7200_hq64.json --check

python3 nikon_movie_patch.py \
  --module /path/to/D7200_0104.dec.modules/b1230_104.bin \
  --config profiles/d7200_hq64.json \
  --out /path/to/D7200_0104.dec.modules/b1230_104.hq64.bin \
  --json /path/to/hq64.json

python3 tools/repack_firmware.py --key keys/key_all.json \
  --firmware /path/to/D7200_0104.bin \
  --replace-module b1230_104.bin=/path/to/D7200_0104.dec.modules/b1230_104.hq64.bin \
  --keep-tags --out /path/to/D7200_0104.hq64.bin
```

### Expected hashes

| File | SHA-256 |
| --- | --- |
| Stock `D7200_0104.bin` | `68cc80ff6308ab1b8cd05d3d13efee5637a0abb384996e60d5e17ffe894e8cec` |
| Patched module `b1230_104.hq64.bin` | `c278c63419f82cacdc62d91670dbb95a75e10e21572464e730000567c37ef4dc` |
| Repacked `D7200_0104.hq64.bin` | `e3c01185813a923fc87090bb175844ae17d677aba575b8070e2d624a01e7be47` |

`--check` should print `changed bytes: 29`. If a stock check fails, **do not
flash**. The hashes assume the same stock image, tool version and profile.

## Other models

| Model | Stock file | Main module | Profile | Packaging |
| --- | --- | --- | --- | --- |
| D7200 C 1.04 | `D7200_0104.bin` | `b1230_104.bin` | `d7200_hq64.json` | A |
| D750 1.15 | `D750_0115.bin` | `b1010_115a.bin` | `d750_hq64.json` | A |
| D810 1.14 | `D810_0114.bin` | `b920_114.bin` | `d810_hq64.json` | A |
| D3400 C 1.13 | `D3400_0113.bin` | `b1480_113.bin` | `d3400_hq64.json` | **B** |

Use the same commands with the module/profile swapped:

```bash
python nikon_movie_patch.py --module <b...>.bin \
  --config profiles/<model>_hq64.json --check
python nikon_movie_patch.py --module <b...>.bin \
  --config profiles/<model>_hq64.json \
  --out <b...>.hq64.bin --json <model>_hq64.json
```

**D3400 is packaging B**: its 32-byte header contains `SHA1(body || K8)` and K8
is unknown. The module-level profile is verified, but the default repack refuses
a stale header. A complete image needs K8, or an explicit
`--allow-stale-header` (the camera may reject it). See
[docs/USAGE.md](docs/USAGE.md).

## What this repository is

`E4_HQ_VID` is a **data-driven** movie-mode patcher for Nikon EXPEED 4 DSLRs:

- patch bitrate fields (`rate_a/rate_b`) in the movie-mode table instead of
  hard-coded byte edits;
- replace UTF-16 menu labels in place, without reflowing the packed language pool;
- check every stock value before writing;
- verify that the final module differs only in the declared fields;
- rebuild directories, CRCs and encryption, then self-validate the container;
- support multiple bodies with profiles and bring up new bodies with a scanner.

It started from the D7200 1080p60 HQ 64 Mbps + `Hq` menu experiment and now
includes D7200, D750, D810 and D3400 profiles plus a generic scan/patch flow.

## Supported models

| Model | Profile | Change | Verification |
| --- | --- | --- | --- |
| D7200 C 1.04 | `d7200_hq64.json` | 1080p60 HQ 64/60 Mbps; `1080 60p Hq` | stock-checked + camera-tested by the author (bitrate/playback OK) |
| D750 1.15 | `d750_hq64.json` | 1080p60 HQ 64/60 Mbps; `1080 60p Hq` | stock-checked; not camera-tested |
| D810 1.14 | `d810_hq64.json` | 1080p60 HQ 64/60 Mbps; `1080 60p Hq` | stock-checked; not camera-tested |
| D3400 C 1.13 | `d3400_hq64.json` | 1080p60 HQ 64/60 Mbps; frame-size + combined `Hq` labels | stock-checked; not camera-tested; packaging B |

“Stock-checked” means the script verified the table entry, rates, label offsets
and lengths. “Camera-tested” means the author flashed it and confirmed bitrate
and playback. They are not the same thing.

## How it works

### Movie-mode table

Nikon EXPEED 4 uses fixed-stride records, typically 22 entries × `0x1C` bytes:

| Offset | Field |
| --- | --- |
| `0x00` | width/height (`height × 65536 + width`) |
| `0x04` | timebase numerator |
| `0x08` | timebase denominator |
| `0x0C` | frame-rate field |
| `0x10` | `rate_a` (HQ/high bitrate) |
| `0x14` | `rate_b` (HQ/high bitrate) |
| `0x18` | flag |

A profile selects a 1-based `entry`; D7200 1080p60 HQ is entry 1. Only
`rate_a/rate_b` change; resolution/timebase/flag stay stock.

### Menu labels

Menu labels are a contiguous UTF-16LE pool. A replacement must have the **same
number of code units**, otherwise every following label shifts. The repository
therefore uses a compact form:

```text
1920x1080; 60p  ->  1080 60p Hq
```

The D7200 menu font has no uppercase `Q` glyph, so `HQ` renders as a placeholder;
lowercase `q` exists in labels such as `Movie quality`, hence `Hq`.

### Checks and repacking

- `nikon_movie_patch.py` reads stock, verifies the entry/labels, then writes;
- it checks that the diff is confined to the declared rate/label ranges;
- `repack_firmware.py` rebuilds the directory, module CRCs and package CRC,
  re-encrypts, and runs `validate_firmware()`;
- packaging B with a stale header digest is refused by default, so the tool does
  not silently produce an image the camera will reject.

## Installation

- Python 3.9+
- NumPy: `python -m pip install -r requirements.txt`
- No firmware or keys are included. Put `key_all.json` in `keys/` (git-ignored)
  or pass `--key`.

## Usage

See [docs/USAGE.md](docs/USAGE.md) for the full workflow, [docs/FAQ.md](docs/FAQ.md)
for common questions, and [CHANGELOG.md](CHANGELOG.md) for changes. Minimal
sequence:

1. decrypt the stock image with `tools/decrypt_dslr2.py` → `*.dec.modules/`;
2. run `nikon_movie_patch.py --check`;
3. run `nikon_movie_patch.py --out`;
4. repack with `tools/repack_firmware.py`;
5. decrypt the output and confirm only the intended module/fields changed.

## Three hard constraints for menu labels

1. **Same length**: the UTF-16 pool is contiguous; pad with spaces.
2. **Glyph must exist**: the camera font is not full Unicode; missing characters
   become boxes. On D7200 uppercase `Q` is missing; lowercase `q` works.
3. **Never touch separators or following strings**: only the declared byte range
   may change; the tool rejects out-of-range diffs.

## D3400 / packaging B

The D3400 header is 32-byte packaging B and contains `SHA1(body || K8)`. K8 is not
available here, so:

- the D3400 **module profile is stock-checked**;
- the default repack refuses to write a complete image with a stale header;
- `--allow-stale-header` bypasses that check, but the camera may reject it;
- until K8 is available, do not treat a D3400 full image as flashable.

## Repository layout

```text
E4_HQ_VID/
  nikon_movie_patch.py      data-driven patcher
  scan_movie_modes.py       read-only table/label scanner
  profiles/                 per-model profiles
  tools/                    decrypt + repack toolchain
  tests/                    stock-check/scanner tests
  docs/                     usage, add-model, FAQ
  keys/                     put key_all.json here (git-ignored)
```

## Tests

```bash
export D7200_MODULE=/path/to/b1230_104.bin
export D750_MODULE=/path/to/b1010_115a.bin
export D810_MODULE=/path/to/b920_114.bin
export D3400_MODULE=/path/to/b1480_113.bin
python -m unittest discover -s tests -v
```

Tests are read-only and skip missing modules. The D7200 test also asserts the
exact SHA of the current patched module.

## Contributing

Profiles, scanner improvements, docs and tests are welcome. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first.

**Do not submit** firmware, decrypted modules, keys, flashable images, personal
data, or anything you do not have the right to distribute. Contributions are
licensed under GPL-3.0 and require a DCO sign-off.

## Security

Report vulnerabilities, key leaks or supply-chain issues privately as described
in [SECURITY.md](SECURITY.md). Do not paste keys or unreleased firmware in a
public issue.

## Legal and licensing

- Code and documentation: **GPL-3.0**, see [LICENSE](LICENSE).
- Third-party tool origins and copyright: see [NOTICE.md](NOTICE.md).
- Full legal notice: see [LEGAL.md](LEGAL.md).
- Code of conduct: see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Again: no firmware or keys are provided; flashing risk, legal compliance and
warranty consequences are the user's responsibility.

## Credits

- [WonderLantern/nikon-fw-key-tool](https://github.com/WonderLantern/nikon-fw-key-tool)
  for the decryption/repack toolchain (GPL-3.0);
- contributors who provided D7200/D750/D810/D3400 modules and test feedback;
- everyone who does this research legally and only on hardware they own.
