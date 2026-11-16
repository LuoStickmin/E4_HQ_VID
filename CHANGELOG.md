# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- Documentation audit: D3400's packaging-B `K8` is no longer "unknown". It was
  recovered as `AF08FBDBB582B587` on 2026-11-15 (see the sibling
  Nikon-Expeed-4-and-5-firmware-tool `docs/k8-dslr.md`); `repack_firmware.py --k8`
  can now verify and recompute the header digest. Camera acceptance remains
  unverified.
- Removed stale "K8 unknown / cannot repack" wording from README, SUPPORT,
  USAGE and FAQ.

## [0.4.0] - 2026-11-15

### Added
- D4S 1.33 profile (`d4s_hq64.json`, table `0x262F48`).
- D5500 1.02 profile (`d5500_hq64.json`, table `0x2D0334`, combined labels).
- D5600 1.20 profile (`d5600_hq64.json`, table `0x301C8C`, combined labels,
  packaging B; K8 recovered as `6FA0738BE53A7DE7`).
- D810A 1.03 profile (`d810a_hq64.json`, table `0x28B940`).
- `module` field in every profile, so the main module is explicit.

### Changed
- Eight profiles now ship: D7200, D750, D810, D810A, D4S, D5500, D5600, D3400.
- Only D7200 is camera-tested; all other profiles are stock-checked, not flashed.
- D5300/D3300 are marked needs-analysis (standard table/labels not found in the
  local samples); D3500 is marked missing-data (no complete firmware/module).

## [0.3.0] - 2026-11-15

### Added
- `SUPPORT.md`: complete EXPEED 4 DSLR support matrix (D4S, D750, D810, D810A,
  D7200, D5300, D5500, D5600, D3300, D3400, D3500) with status, packaging and
  limitations.
- README “最近更新 / Recent changes” short changelog and the 11-model overview
  table.

### Changed
- README supported-model section now links to `SUPPORT.md` and separates
  camera-tested, stock-checked, scanner-ready and needs-analysis models.
- Clarified that D4S/D810A/D5300/D5500/D5600/D3300/D3500 have no profile yet.

## [0.2.1] - 2026-11-13

### Added
- Bilingual README (`README.md`, `README.en.md`) with the disclaimer first and
  a copy-paste D7200 reproduction block.
- `CONTRIBUTING.md` with the GPL-3.0 open-source declaration, DCO 1.1,
  profile checklist and legal rules.
- `LEGAL.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`.
- `docs/FAQ.md`.
- GitHub issue/PR templates and `.gitattributes`.

## [0.2.0] - 2026-11-13

### Added
- D3400 C 1.13 profile (`profiles/d3400_hq64.json`) derived from the official
  update, SHA-256 `4310b873…2f37a`.
- D3400 combined "Movie frame size/quality" label patches (four labels).
- Scanner test case for D3400.
- Packaging-B warning for D3400 (header digest / K8 unknown).

### Changed
- README supported-model matrix now marks D3400 as a real, stock-checked
  profile rather than a template.
- D3400 module patch changes 69 bytes (8 rate bytes + 61 label bytes).

### Removed
- `profiles/d3400_template.json` (replaced by the real profile).

## [0.1.0] - 2026-11-13

### Added
- Initial `E4_HQ_VID` repository.
- `nikon_movie_patch.py`: data-driven movie-rate + UTF-16 label patcher with
  stock checks and diff-scope verification.
- `scan_movie_modes.py`: read-only movie-table and label scanner with profile
  skeleton emission.
- Profiles for D7200 C 1.04, D750 1.15 and D810 1.14 (1080p60 HQ 64/60 Mbps,
  `1080 60p Hq`).
- Decrypt/repack toolchain under `tools/`.
- Tests for the patcher, profiles and scanner.
- Usage and add-model documentation.
