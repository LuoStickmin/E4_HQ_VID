# Keys are not included

This repository does not ship `key_all.json`, firmware images, decrypted
modules, or patched images.

Put your own `key_all.json` in this directory (it is git-ignored) or pass an
absolute path with `--key`.  The key must cover the model/firmware you are
working on; otherwise `decrypt_dslr2.py` / `repack_firmware.py` will fail.

Do not commit keys or firmware.  A packaging-B `K8` JSON (for example
`d3400_0113_k8.json`, see `docs/USAGE.md`) may also be placed here; this
repository ships no such files.
