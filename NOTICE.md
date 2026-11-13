# NOTICE

## Copyright and license

- `nikon_movie_patch.py`, `scan_movie_modes.py`, the profiles, tests and
  documentation are original work for this repository, licensed under
  **GPL-3.0** (see `LICENSE`).
- `tools/repack_firmware.py`, `tools/decrypt_firmware.py`,
  `tools/decrypt_dslr2.py` and `tools/decrypt_dslr.py` are adapted from
  [WonderLantern/nikon-fw-key-tool](https://github.com/WonderLantern/nikon-fw-key-tool)
  (GPL-3.0).  Their copyright remains with the original authors.
- Third-party names and trademarks, including Nikon, EXPEED, D7200, D750, D810
  and D3400, belong to their respective owners.

## No affiliation

This repository is not affiliated with, authorized by, sponsored by, or endorsed
by Nikon Corporation.  It is an independent research/interoperability project.

## No firmware, keys, or images

This repository contains **no** Nikon firmware, decrypted modules, keys,
`key_all.json`, or flashable images.  The D3400 profile was derived from a
locally obtained official update, but neither the update nor the decrypted module
is distributed here.

## Third-party toolchain

The decrypt/repack tools implement container parsing, CRC, encryption and
repacking logic adapted from the GPL-3.0 `nikon-fw-key-tool`.  If you redistribute
this repository or a modified version, keep the GPL-3.0 notices and make the
corresponding source available as required by the license.

## Legal

See `LEGAL.md` for the full disclaimer and legal notice, and `CONTRIBUTING.md`
for contribution licensing and the DCO.
