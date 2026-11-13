# Contributing to E4_HQ_VID

[中文摘要](#中文摘要) · [Open-source declaration](#open-source-declaration) ·
[Legal statement](#legal-statement) · [What we accept](#what-we-accept) ·
[Profile checklist](#profile-checklist) · [DCO](#developer-certificate-of-origin-dco)

## 中文摘要

- 欢迎提交 profile、扫描器改进、文档和测试。
- 贡献按 **GPL-3.0** 授权；不需要 CLA，但每个 commit 必须用 `git commit -s`
  做 **DCO 1.1** 签名。
- **禁止提交**固件、解密模块、密钥、可刷写镜像、个人信息或任何你无权分发的内容。
- 新机型 profile 必须附 stock 校验结果、改动的字节数、封装类型（A/B）和是否上机。
- 法律合规、刷机风险由贡献者和使用者自行承担；详见 [LEGAL.md](LEGAL.md)。

## Open-source declaration

By contributing you agree that:

1. Your contribution is licensed under the **GNU General Public License v3.0**
   (the repository license), and you have the right to license it that way.
2. You are not granting the maintainers any additional copyright assignment;
   there is **no CLA**.
3. Your contribution is your own work, or is compatible with GPL-3.0 and
   properly attributed.
4. You will sign off every commit under the **Developer Certificate of Origin 1.1** (see below).
5. You will not contribute firmware, decrypted firmware modules, keys,
   flashable images, or other material you do not have the right to distribute.

Documentation is licensed under GPL-3.0 together with the code unless a file
says otherwise.

## Legal statement

This project is **not affiliated with, authorized by, or endorsed by Nikon**.
Nikon, EXPEED and related marks belong to their respective owners.

- Do not upload Nikon firmware or decrypted modules to issues, pull requests,
  discussions or CI artifacts.
- Do not upload `key_all.json`, key material, or anything derived from it.
- Do not request, link to, or provide pirated firmware or cracked keys.
- Reverse engineering and firmware modification are regulated differently
  across jurisdictions. You are responsible for complying with the law where
  you live, including copyright, contract, export-control and
  anti-circumvention rules.
- Contributions must not be intended to circumvent copyright protection or
  technological protection measures; the project is for research,
  interoperability and format analysis on hardware you own.
- There is **no warranty**. Flashing modified firmware can brick hardware, void
  warranties and destroy data. Maintainers and contributors accept no liability.
- See [LEGAL.md](LEGAL.md) for the full notice.

If you are unsure whether a contribution is lawful, open an issue **without**
attaching the questionable material and ask first.

## What we accept

- New model profiles (`profiles/<model>_hq64.json`) with stock checks.
- Scanner improvements for finding movie tables and UTF-16 labels.
- Patcher improvements: better validation, clearer errors, safe diff checks.
- Tests that use synthetic data or locally supplied modules (never commit the
  module itself).
- Documentation, translations, FAQ entries and reproduction reports.
- Repack/decrypt fixes that preserve stock round-trip behavior.

## What we do not accept

- Firmware images, `.dec` files, `*.dec.modules/`, keys, or flashable outputs.
- Requests for keys, cracked firmware, or help bypassing licensing.
- Changes that weaken stock checks or silently allow out-of-range diffs.
- Changes that make the repacker ignore a stale packaging-B header by default.
- Personal data, camera serial numbers, or private test footage.
- Claims that a profile is camera-tested without evidence.

## Profile checklist

A profile PR should include:

- [ ] Model and exact firmware version (`D7200 C 1.04`, `D3400 C 1.13`, ...).
- [ ] Stock image SHA-256 and main module name.
- [ ] Movie-table offset, stride, field layout, and 1-based entry.
- [ ] Stock values for resolution/timebase/frame-rate/rates/flag.
- [ ] Label offsets, stock strings, replacement strings, and code-unit lengths.
- [ ] `--check` output and the changed-byte count.
- [ ] Packaging class (A/B) and whether a complete image can be produced.
- [ ] Whether it was camera-tested, and what was measured (bitrate, playback,
      duration, stripes, overheating, card errors).
- [ ] Confirmation that no firmware, module, key or image is attached.

A typical profile patch is small: D7200/D750/D810 change 29 bytes; D3400 changes
69 bytes because it has both frame-size and combined quality labels.

## Code style and tests

- Python 3.9+, standard library first; new runtime dependencies need a reason.
- Keep the patcher data-driven; model-specific offsets belong in JSON profiles,
  not in Python branches.
- Never write to the stock module; `--out` must be a different path.
- Add a test for new validation behavior.
- Run:

```bash
python -m unittest discover -s tests -v
```

Set `D7200_MODULE`, `D750_MODULE`, `D810_MODULE`, `D3400_MODULE` to local stock
modules; tests skip missing models.

## Pull request process

1. Open an issue for a new model/profile before a large PR.
2. Fork, create a topic branch, keep commits focused.
3. Sign off each commit: `git commit -s -m "..."`.
4. Describe the stock verification and test results in the PR.
5. CI/most tests only use synthetic or locally supplied data; never attach
   firmware.
6. A maintainer reviews for correctness, scope and legal hygiene.

## Developer Certificate of Origin (DCO)

Every commit must contain a `Signed-off-by` line certifying the DCO 1.1:

```text
Signed-off-by: Your Name <you@example.com>
```

Use `git commit -s`. The full DCO 1.1 is available at
<https://developercertificate.org/>. By signing off you certify that you have
the right to submit the contribution under the repository license.

## Security

Do not report key leaks or vulnerabilities in a public issue. See
[SECURITY.md](SECURITY.md).

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
