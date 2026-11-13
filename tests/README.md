# Tests

The tests are read-only and skip any model whose decrypted module is not
available.

```bash
# from the repository root
export D7200_MODULE=/path/to/b1230_104.bin
export D750_MODULE=/path/to/b1010_115a.bin
export D810_MODULE=/path/to/b920_114.bin
export D3400_MODULE=/path/to/b1480_113.bin

python -m unittest discover -s tests -v
```

PowerShell:

```powershell
$env:D7200_MODULE = 'C:\...\b1230_104.bin'
$env:D750_MODULE  = 'C:\...\b1010_115a.bin'
$env:D810_MODULE  = 'C:\...\b920_114.bin'
$env:D3400_MODULE = 'C:\...\b1480_113.bin'
python -m unittest discover -s tests -v
```

The D7200 test also asserts the exact module SHA of the current flashed state
(`b1230_104.hq64b.bin`).
