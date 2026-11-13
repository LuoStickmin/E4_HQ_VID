# Keys are not included

This repository does not ship `key_all.json`, firmware images, decrypted
modules, or patched images.

Put your own `key_all.json` in this directory (it is git-ignored) or pass an
absolute path with `--key`.  The key must cover the model/firmware you are
working on; otherwise `decrypt_dslr2.py` / `repack_firmware.py` will fail.

Do not commit keys or firmware.
