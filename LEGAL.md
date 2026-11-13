# 法律声明 / Legal Notice

[中文](#中文) · [English](#english)

> 本文件不是法律意见。它是项目的风险与合规说明；如不确定，请咨询你所在
> 司法辖区的律师。

## 中文

### 1. 非关联声明

本项目与尼康（Nikon Corporation）及其关联公司**没有任何关联**，未获其授权、
赞助或背书。Nikon、EXPEED、D7200、D750、D810、D3400 等名称和商标归其各自
权利人所有。本仓库仅用于说明和互操作性研究，不暗示尼康认可本项目。

### 2. 不提供固件、密钥或镜像

本仓库**不包含**：

- 尼康固件镜像（如 `D7200_0104.bin`）；
- 解密后的模块（`*.dec`、`*.dec.modules/`）；
- `key_all.json` 或任何密钥材料；
- 可刷写的修改镜像。

你需要自行合法取得固件和密钥。仓库中的脚本只处理你提供的本地文件。

### 3. 风险

修改、重封包和刷写固件可能导致：

- 相机变砖、无法开机或无法恢复；
- 丢失保修、服务和支持；
- 丢失照片、视频或设置；
- 过热、存储卡错误、录制中断或其他硬件问题；
- 违反当地法律、合同或平台政策。

**你自行承担全部风险。** 刷机前请保留原厂固件、备份数据，并确认有恢复路径。
作者和贡献者不对任何直接、间接、附带或后果性损失承担责任。

### 4. 法律合规

固件修改和逆向工程在不同司法辖区的合法性不同。你可能需要遵守：

- 著作权法和软件许可；
- 反规避条款（如美国 DMCA §1201、欧盟信息社会指令的相关条款）；
- 合同/保修条款；
- 出口管制和制裁规则；
- 商标、不正当竞争和消费者保护法；
- 当地关于设备改装、无线电和产品安全的规定。

本项目用于自己拥有设备上的研究、互操作、格式分析和教育目的，**不意图**
规避著作权保护或技术保护措施，也不鼓励盗版、破解付费功能或规避许可。
你应确保使用方式在所在辖区合法。如果法律不允许，请不要使用本项目。

### 5. 许可

- 代码和文档：**GNU General Public License v3.0**，见 [LICENSE](LICENSE)。
- 第三方工具：见 [NOTICE.md](NOTICE.md)；其版权归原作者，按 GPL-3.0 分发。
- 贡献：按 GPL-3.0 授权，并要求 DCO 1.1 签名，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

GPL-3.0 不授予你任何尼康固件、商标、专利或其他第三方权利。

### 6. 隐私

本仓库的脚本不包含遥测、分析或网络回传。你运行脚本时处理的文件保留在本地；
但你的 shell 历史、日志、issue/PR 内容可能包含路径或元数据，请自行清理。
不要在公开 issue 中粘贴密钥、序列号、未公开固件或个人素材。

### 7. 责任限制

在适用法律允许的最大范围内，作者和贡献者不对使用或无法使用本项目造成的
任何损害承担责任，包括但不限于设备损坏、数据丢失、利润损失、业务中断或
法律费用。本项目按“现状”提供，不附带任何明示或默示担保。

### 8. 联系

法律或安全问题请通过仓库的私密安全报告渠道联系维护者，不要在公开 issue 中
披露敏感材料。见 [SECURITY.md](SECURITY.md)。

## English

### 1. No affiliation

This project is **not affiliated with, authorized by, sponsored by, or endorsed
by Nikon Corporation** or its affiliates. Nikon, EXPEED, D7200, D750, D810,
D3400 and related names and marks belong to their respective owners. This
repository is for documentation and interoperability research and does not imply
Nikon's approval.

### 2. No firmware, keys, or images

This repository does **not** contain:

- Nikon firmware images (for example `D7200_0104.bin`);
- decrypted modules (`*.dec`, `*.dec.modules/`);
- `key_all.json` or any key material;
- flashable modified images.

You must obtain firmware and keys legally yourself. The scripts operate only on
local files you provide.

### 3. Risk

Modifying, repacking or flashing firmware can:

- brick the camera or make it unable to boot/recover;
- void the warranty, service and support;
- destroy photos, videos or settings;
- cause overheating, card errors, recording interruptions or other hardware
  problems;
- violate local law, contracts or platform policies.

**You assume all risk.** Keep the stock firmware, back up your data, and confirm a
recovery path before flashing. The authors and contributors accept no liability
for direct, indirect, incidental or consequential loss.

### 4. Legal compliance

Firmware modification and reverse engineering are regulated differently across
jurisdictions. You may need to comply with:

- copyright law and software licenses;
- anti-circumvention provisions (for example DMCA §1201 in the United States and
  related provisions of the EU Information Society Directive);
- contract and warranty terms;
- export-control and sanctions rules;
- trademark, unfair-competition and consumer-protection law;
- local rules on device modification, radio and product safety.

This project is for research, interoperability, format analysis and education on
hardware you own. It is **not intended** to circumvent copyright protection or
technological protection measures, and it does not encourage piracy, paid-feature
unlocking or license circumvention. You are responsible for ensuring your use is
lawful where you live. If it is not, do not use the project.

### 5. Licensing

- Code and documentation: **GNU General Public License v3.0**, see
  [LICENSE](LICENSE).
- Third-party tools: see [NOTICE.md](NOTICE.md); their copyright remains with
  their authors and they are distributed under GPL-3.0.
- Contributions: licensed under GPL-3.0 with a DCO 1.1 sign-off, see
  [CONTRIBUTING.md](CONTRIBUTING.md).

GPL-3.0 grants you no rights in Nikon firmware, trademarks, patents or other
third-party rights.

### 6. Privacy

The scripts contain no telemetry, analytics or network exfiltration. Files you
process stay local. Your shell history, logs, issues and pull requests may still
contain paths or metadata; sanitize them. Do not paste keys, serial numbers,
unreleased firmware or private footage into public issues.

### 7. Limitation of liability

To the maximum extent permitted by law, the authors and contributors are not
liable for any damages arising from the use or inability to use this project,
including device damage, data loss, lost profits, business interruption or legal
costs. The project is provided “as is”, without express or implied warranties.

### 8. Contact

For legal or security matters, use the repository's private security-reporting
channel; do not disclose sensitive material in a public issue. See
[SECURITY.md](SECURITY.md).
