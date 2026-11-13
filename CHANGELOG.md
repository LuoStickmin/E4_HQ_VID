# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Bilingual README (`README.md`, `README.en.md`) with the disclaimer first and
  a copy-paste D7200 reproduction block.
- `CONTRIBUTING.md` with the GPL-3.0 open-source declaration, DCO 1.1,
  profile checklist and legal rules.
- `LEGAL.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`.
- `docs/FAQ.md`.

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
