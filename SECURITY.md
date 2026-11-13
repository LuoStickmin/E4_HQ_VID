# Security Policy / 安全策略

[中文摘要](#中文摘要) · [English](#english)

## 中文摘要

- 支持最新 `main` 分支；历史版本不保证修复。
- 请通过 GitHub 仓库的 **Security → Report a vulnerability** 私下报告，不要开公开
  issue。
- **不要**在报告里附带固件、解密模块、`key_all.json`、序列号或个人素材；用
  合成数据或最小复现。
- 范围：脚本的校验绕过、越界写、重封包 CRC/加密错误、恶意 profile、路径
  处理、供应链问题。
- 相机固件本身的漏洞、用户刷机导致的变砖、法律问题不在本安全策略范围内。

## English

### Supported versions

Only the latest `main` branch is supported. Older commits may not receive fixes.
There are no binary releases; use the repository at a pinned commit if you need
reproducibility.

### Reporting a vulnerability

Please use **GitHub Security Advisories**:

1. Open the repository's **Security** tab.
2. Choose **Report a vulnerability**.
3. Describe the issue privately.

Do **not** open a public issue for a security problem. If GitHub private reporting
is unavailable, contact the maintainer through the GitHub profile listed on the
repository and ask for a private channel.

### What to include

- Affected script(s) and commit/branch.
- Python version and OS.
- A minimal, synthetic reproduction (no firmware, no keys, no personal data).
- Impact: validation bypass, out-of-range write, incorrect CRC/encryption,
  path traversal, malicious profile, dependency issue, etc.
- Whether the issue can cause a flashable but invalid image.

**Never attach** firmware images, decrypted modules, `key_all.json`, key
material, camera serial numbers, or private footage. If a proof of concept needs
a real module, reduce it to synthetic bytes or a redacted snippet.

### In scope

- `nikon_movie_patch.py` stock-check or diff-scope bypass.
- `scan_movie_modes.py` crashes or unsafe output on untrusted modules.
- `tools/repack_firmware.py` / decrypt tools: incorrect CRC, encryption,
  directory handling, truncation, path handling.
- Profile handling: path traversal, arbitrary write, unbounded allocation.
- Supply-chain or dependency issues in the repository.
- Documentation that could cause a user to flash an invalid image.

### Out of scope

- Vulnerabilities in Nikon camera firmware or Nikon software.
- Bricking caused by flashing a modified image, wrong model, or interrupted
  update.
- Legal questions about reverse engineering or firmware modification.
- Issues that require keys or firmware we do not have.
- Social engineering or physical access attacks.

### Response

We aim to acknowledge a report within 7 days and to provide a status update
within 30 days. This is a volunteer project; there is no bug bounty. We will
credit reporters who want credit, after a fix or coordinated disclosure.

### Safe harbor

We will not pursue legal action for good-faith security research that:

- stays within this repository's scripts and your own hardware;
- avoids privacy violations, data destruction and service disruption;
- reports the issue privately and gives us reasonable time to fix it;
- does not exfiltrate keys, firmware or user data.

This safe harbor does not override the law or third-party rights.
