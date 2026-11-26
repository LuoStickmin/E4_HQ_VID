# E4_HQ_VID

[中文](README.md) | [English](README.en.md) | [Support matrix](SUPPORT.md)

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
| D810A 1.03 | `D810A_0103.bin` | `b1410_102b.bin` | `d810a_hq64.json` | A |
| D4S 1.33 | `D4S_0133.bin` | `b1140_133f.bin` | `d4s_hq64.json` | A |
| D5500 1.02 | `D5500_0102.bin` | `b1120_102.bin` | `d5500_hq64.json` | A |
| D5600 1.20 | `D5600_0120.bin` | `b1530_120.bin` | `d5600_hq64.json` | **B** |
| D3400 C 1.13 | `D3400_0113.bin` | `b1480_113.bin` | `d3400_hq64.json` | **B** |

Use the same commands with the module/profile swapped:

```bash
python nikon_movie_patch.py --module <b...>.bin \
  --config profiles/<model>_hq64.json --check
python nikon_movie_patch.py --module <b...>.bin \
  --config profiles/<model>_hq64.json \
  --out <b...>.hq64.bin --json <model>_hq64.json
```

**D3400 is packaging B**: its 32-byte header contains `SHA1(body || K8)`. The
D3400 K8 was recovered on 2026-11-15 as `AF08FBDBB582B587`; the module-level
profile is verified, and a complete image has been repacked with `--k8` and
decrypted again to confirm container-level consistency. Camera acceptance is
still unverified. See [docs/USAGE.md](docs/USAGE.md) and the author's
[k8-dslr record](https://github.com/LuoStickmin/Nikon-Expeed-4-and-5-firmware-tool/blob/main/docs/k8-dslr.en.md).

**D5600 is also packaging B**: its K8 was recovered as `6FA0738BE53A7DE7`; a
complete image has been repacked with `--k8` and decrypted again to confirm
container-level consistency. Camera acceptance is still unverified.

## Movie time limits (D7200/D750)

`time_limits/` contains a read-only scanner and data patcher for the E4 movie
time-limit table (30 u32 milliseconds; D750 1.15 at `0x2F2104`, D7200 1.04 at
`0x2DDD98`), plus `time_limit_patch.py`, which can set the whole table to 59:59.

- Models and usage: [time_limits/README.md](time_limits/README.md).
- D7200 `d7200_hq64_50p.json` raises both 1080p60 and 1080p50 HQ to 64/60;
  the 50p image `93974982…305288b` is container-verified only.
- The table does **not** lift the ~4 GB per-file cap or fix the camera's
  `NCDT` playback requirement; see [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

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
includes eight profiles (D7200/D750/D810/D810A/D3400/D4S/D5500/D5600) plus a
generic scan/patch flow.

## Supported models

There are 11 EXPEED 4 DSLRs. Eight have profiles ready; three are blocked by
firmware/layout limitations. Full status, packaging and notes: [SUPPORT.md](SUPPORT.md).

> **Rigor note: only D7200 and D750 have been camera-tested by the author.**
> All other profiles are stock-checked, not flashed, and are not a guarantee
> that the camera accepts the image.

| Model | Profile | Status |
| --- | --- | --- |
| D7200 C 1.04 | `d7200_hq64.json` | ✅ camera-tested; 64/60 Mbps + `Hq` |
| D750 1.15 | `d750_hq64.json` | ✅ camera-tested; 64/60 Mbps + `Hq` |
| D810 1.14 | `d810_hq64.json` | 🟩 stock-checked; 64/60 Mbps + `Hq` |
| D810A 1.03 | `d810a_hq64.json` | 🟩 stock-checked; 64/60 Mbps + `Hq` |
| D4S 1.33 | `d4s_hq64.json` | 🟩 stock-checked; 64/60 Mbps + `Hq` |
| D5500 1.02 | `d5500_hq64.json` | 🟩 stock-checked; 64/60 Mbps + `Hq` |
| D5600 1.20 | `d5600_hq64.json` | 🟩 stock-checked; packaging B, K8 recovered, full image container-tested |
| D3400 C 1.13 | `d3400_hq64.json` | 🟩 stock-checked; packaging B, K8 recovered, full image container-tested |
| D5300 | — | 🟧 needs analysis; local 1.03 sample did not auto-detect the standard table/labels |
| D3300 | — | 🟧 needs analysis; local 1.02 sample did not auto-detect the standard table/labels |
| D3500 | — | 🟥 missing complete firmware/module; no profile yet |

Legend:

- ✅ **camera-tested**: flashed by the author; bitrate/playback confirmed;
- 🟩 **stock-checked**: profile verified against stock table/labels; not flashed;
- 🟨 **scanner-ready**: no profile; run `scan_movie_modes.py` on a decrypted
  module and add one;
- 🟧 **needs analysis**: a local sample exists, but the standard 0x1C table/UTF-16
  labels were not auto-detected;
- 🟥 **missing data**: no complete firmware/module is available, so no profile;
- ⛔ **out of scope**: D5/D500/D7500/D850 are EXPEED 5; Z series and Nikon 1 are
  different platforms.

### Recent changes

- **2026-11-16** — **D750 1.15 camera-tested and passed** (1080p60 HQ
  64/60 Mbps + `Hq`); D7200 and D750 are now the two camera-tested profiles.
- **2026-11-15** — added D4S/D5500/D5600/D810A profiles (stock-checked);
  D5300/D3300 are needs-analysis, D3500 is missing firmware. Eight profiles total.
- **2026-11-15** — added the full EXPEED 4 support matrix
  [SUPPORT.md](SUPPORT.md); D3400's K8 was recovered as `AF08FBDBB582B587`, so
  `--k8` can recompute the digest, but camera acceptance is unverified.
- **2026-11-15** — documentation audit: removed the stale "D3400 K8 unknown"
  entry.
- **2026-11-13** — D3400 C 1.13 profile; bilingual README, CONTRIBUTING, LEGAL,
  SECURITY, CODE_OF_CONDUCT, CHANGELOG and FAQ.
- **2026-11-13** — initial D7200/D750/D810 profiles, scanner and
  decrypt/repack toolchain.

Full history: [CHANGELOG.md](CHANGELOG.md).

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

The D3400 header is 32-byte packaging B and contains `SHA1(body || K8)`. Its K8
was recovered on 2026-11-15 as `AF08FBDBB582B587`, so:

- the D3400 **module profile is stock-checked**;
- a complete image can be verified and the digest recomputed with
  `repack_firmware.py --k8 <k8.json>`;
- without `--k8` the default repack still refuses to write a stale header;
  `--allow-stale-header` is only for CRC/QEMU tests;
- a correct digest still does not prove the camera accepts the image.

## Repository layout

```text
E4_HQ_VID/
  nikon_movie_patch.py      data-driven patcher
  scan_movie_modes.py       read-only table/label scanner
  profiles/                 per-model profiles
  tools/                    decrypt + repack toolchain
  tests/                    stock-check/scanner tests
  docs/                     usage, add-model, FAQ
  SUPPORT.md                full EXPEED 4 support matrix
  keys/                     put key_all.json here (git-ignored)
```

## Tests

```bash
export D7200_MODULE=/path/to/b1230_104.bin
export D750_MODULE=/path/to/b1010_115a.bin
export D810_MODULE=/path/to/b920_114.bin
export D3400_MODULE=/path/to/b1480_113.bin
export D4S_MODULE=/path/to/b1140_133f.bin
export D5500_MODULE=/path/to/b1120_102.bin
export D5600_MODULE=/path/to/b1530_120.bin
export D810A_MODULE=/path/to/b1410_102b.bin
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
- contributors who provided D7200/D750/D810/D810A/D4S/D5500/D5600/D3400 modules and test feedback;
- everyone who does this research legally and only on hardware they own.
