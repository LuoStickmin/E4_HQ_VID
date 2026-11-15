# E4_HQ_VID

[中文](README.md) | [English](README.en.md) | [支持矩阵](SUPPORT.md)

> ## ⚠️ 免责声明
>
> - 本项目与尼康（Nikon）没有任何关联，未获尼康授权或背书；Nikon、EXPEED 等是其各自权利人的商标。
> - 仓库**不包含**任何固件、解密模块、密钥或可刷写镜像。你需要自行合法取得固件和 `key_all.json`。
> - 修改、重封包、刷写固件可能导致相机变砖、失去保修、数据丢失，甚至违反当地法律。**风险由使用者自行承担。**
> - 本项目用于自己拥有设备上的研究、互操作和格式分析，不意图规避版权保护或技术保护措施。请在所在司法辖区法律允许的范围内使用。
> - 作者和贡献者不对任何直接或间接损失负责。刷机前请保留原厂固件和可恢复方案。
>
> 完整条款见 [LEGAL.md](LEGAL.md)。继续使用即表示你已阅读并同意这些条款。

## 直接复现：D7200 C 1.04 当前状态

目标：1080p60 **HQ** 码率 `42/35 → 64/60 Mbps`，菜单显示 `1080 60p Hq`。

需要：`D7200_0104.bin`（原厂 C 1.04）和覆盖该固件的 `key_all.json`。

### Windows PowerShell

```powershell
git clone https://github.com/LuoStickmin/E4_HQ_VID.git
cd E4_HQ_VID
python -m pip install -r requirements.txt
mkdir keys
copy C:\path\to\key_all.json keys\key_all.json

# 1. 解密
python tools\decrypt_dslr2.py --key keys\key_all.json `
  --firmware C:\path\to\D7200_0104.bin `
  --out C:\path\to\D7200_0104.dec

# 2. 只检查 stock，不写文件
python nikon_movie_patch.py `
  --module C:\path\to\D7200_0104.dec.modules\b1230_104.bin `
  --config profiles\d7200_hq64.json --check

# 3. 写补丁模块
python nikon_movie_patch.py `
  --module C:\path\to\D7200_0104.dec.modules\b1230_104.bin `
  --config profiles\d7200_hq64.json `
  --out C:\path\to\D7200_0104.dec.modules\b1230_104.hq64.bin `
  --json C:\path\to\hq64.json

# 4. 重封包
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

### 期望校验值

| 文件 | SHA-256 |
| --- | --- |
| 原厂 `D7200_0104.bin` | `68cc80ff6308ab1b8cd05d3d13efee5637a0abb384996e60d5e17ffe894e8cec` |
| 补丁模块 `b1230_104.hq64.bin` | `c278c63419f82cacdc62d91670dbb95a75e10e21572464e730000567c37ef4dc` |
| 重封包 `D7200_0104.hq64.bin` | `e3c01185813a923fc87090bb175844ae17d677aba575b8070e2d624a01e7be47` |

`--check` 应显示 `changed bytes: 29`。如果 stock 校验失败，**不要继续刷写**。
SHA 一致的前提是同一原厂固件、同一工具版本和同一 profile。

## 其他机型

| 机型 | 原厂文件 | 主模块 | Profile | 封装 |
| --- | --- | --- | --- | --- |
| D7200 C 1.04 | `D7200_0104.bin` | `b1230_104.bin` | `d7200_hq64.json` | A |
| D750 1.15 | `D750_0115.bin` | `b1010_115a.bin` | `d750_hq64.json` | A |
| D810 1.14 | `D810_0114.bin` | `b920_114.bin` | `d810_hq64.json` | A |
| D810A 1.03 | `D810A_0103.bin` | `b1410_102b.bin` | `d810a_hq64.json` | A |
| D4S 1.33 | `D4S_0133.bin` | `b1140_133f.bin` | `d4s_hq64.json` | A |
| D5500 1.02 | `D5500_0102.bin` | `b1120_102.bin` | `d5500_hq64.json` | A |
| D5600 1.20 | `D5600_0120.bin` | `b1530_120.bin` | `d5600_hq64.json` | **B** |
| D3400 C 1.13 | `D3400_0113.bin` | `b1480_113.bin` | `d3400_hq64.json` | **B** |

把上面命令中的模块名/profile 换掉即可：

```bash
python nikon_movie_patch.py --module <b...>.bin \
  --config profiles/<model>_hq64.json --check
python nikon_movie_patch.py --module <b...>.bin \
  --config profiles/<model>_hq64.json \
  --out <b...>.hq64.bin --json <model>_hq64.json
```

**D3400 是 packaging B**：32 字节头含 `SHA1(body || K8)`。D3400 的 K8 已于
2026-11-15 恢复为 `AF08FBDBB582B587`；模块级 profile 已验证，完整镜像已用
`--k8` 做重封包 + 解密回读验证（容器层一致）。相机是否接受重封包仍未做
真机验证。详见 [docs/USAGE.md](docs/USAGE.md) 与同作者的
[k8-dslr 记录](https://github.com/LuoStickmin/Nikon-Expeed-4-and-5-firmware-tool/blob/main/docs/k8-dslr.md)。

## 这个仓库是什么

`E4_HQ_VID` 是一个面向 EXPEED 4 尼康单反的**数据驱动**电影模式补丁工具集：

- 修改电影模式表中的码率字段（`rate_a/rate_b`），而不是硬编码字节；
- 在同长度 UTF-16 菜单池中替换标签，不移动后续字符串；
- 每个改动先校验 stock 值，最后校验差异只落在声明字段；
- 用重封包工具重建目录、CRC、加密，并做容器自校验；
- 用 profile 支持多机型，用扫描器支持新机型。

它最早来自 D7200 1080p60 HQ 64 Mbps + 菜单 `Hq` 的实测需求；现在包含
D7200/D750/D810/D810A/D3400/D4S/D5500/D5600 八个 profile，以及通用扫描/补丁流程。

## 支持的机型

EXPEED 4 单反共 11 款；已有 profile 的 8 款可以直接用，剩余 3 款受固件/布局限制。
完整状态、封装和备注见 [SUPPORT.md](SUPPORT.md)。

> **严谨说明：只有 D7200 由作者真机实测。** 其他机型都是 stock 校验，不等于
> 已经在相机上验证，更不等于“可安全刷写”。

| 机型 | Profile | 状态 |
| --- | --- | --- |
| D7200 C 1.04 | `d7200_hq64.json` | ✅ 真机实测；64/60 Mbps + `Hq` |
| D750 1.15 | `d750_hq64.json` | 🟩 stock 校验；64/60 Mbps + `Hq` |
| D810 1.14 | `d810_hq64.json` | 🟩 stock 校验；64/60 Mbps + `Hq` |
| D810A 1.03 | `d810a_hq64.json` | 🟩 stock 校验；64/60 Mbps + `Hq` |
| D4S 1.33 | `d4s_hq64.json` | 🟩 stock 校验；64/60 Mbps + `Hq` |
| D5500 1.02 | `d5500_hq64.json` | 🟩 stock 校验；64/60 Mbps + `Hq` |
| D5600 1.20 | `d5600_hq64.json` | 🟩 stock 校验；packaging B，该机型 K8 未恢复 |
| D3400 C 1.13 | `d3400_hq64.json` | 🟩 stock 校验；packaging B，K8 已恢复，完整镜像容器层已验证 |
| D5300 | — | 🟧 待分析；本地 1.03 样本未自动识别标准表/标签 |
| D3300 | — | 🟧 待分析；本地 1.02 样本未自动识别标准表/标签 |
| D3500 | — | 🟥 缺完整固件/模块，暂时无法做 profile |

状态说明：

- ✅ **真机实测**：作者已刷入并确认码率/回放；
- 🟩 **stock 校验**：profile 核对过原厂表项、码率、标签偏移/长度，但未上机；
- 🟨 **scanner-ready**：没有 profile，可用 `scan_movie_modes.py` 在解密模块上
  定位表和标签，再写 profile；
- 🟧 **待分析**：有本地样本，但标准 0x1C 表/UTF-16 标签没有自动识别；
- 🟥 **缺数据**：没有可用完整固件/模块，无法生成 profile；
- ⛔ **不在范围**：D5/D500/D7500/D850 是 EXPEED 5，Z 系列/Nikon 1 是不同平台。

### 最近更新

- **2026-11-15** — 新增 D4S/D5500/D5600/D810A 四个 profile（stock 校验）；
  D5300/D3300 标记为待分析，D3500 标记为缺完整固件。当前共 8 个 profile，
  **只有 D7200 真机实测**。
- **2026-11-15** — 新增完整 EXPEED 4 支持矩阵 [SUPPORT.md](SUPPORT.md)；
  D3400 K8 已恢复为 `AF08FBDBB582B587`，`--k8` 路径可用，但相机接受度未验证。
- **2026-11-15** — 文档复核：移除“D3400 K8 未知”的过期条目。
- **2026-11-13** — D3400 C 1.13 profile；双语 README、CONTRIBUTING、LEGAL、
  SECURITY、CODE_OF_CONDUCT、CHANGELOG、FAQ。
- **2026-11-13** — 初始 D7200/D750/D810 profile、扫描器、解密/重封包工具链。

完整历史见 [CHANGELOG.md](CHANGELOG.md)。

## 工作原理

### 电影模式表

尼康 EXPEED 4 的电影模式表是固定步长记录，典型为 22 项 × `0x1C` 字节：

| 偏移 | 字段 |
| --- | --- |
| `0x00` | 宽高（`height × 65536 + width`） |
| `0x04` | 时基分子 |
| `0x08` | 时基分母 |
| `0x0C` | 帧率字段 |
| `0x10` | `rate_a`（HQ/高码率） |
| `0x14` | `rate_b`（HQ/高码率） |
| `0x18` | flag |

profile 用 1-based `entry` 指定表项，例如 D7200 的 1080p60 HQ 是 entry 1。
补丁只改 `rate_a/rate_b`，不动分辨率/时基/flag。

### 菜单标签

菜单标签是连续的 UTF-16LE 池。替换必须**同字符数**，否则后面的标签会整体
错位。因此本仓库使用紧凑写法：

```text
1920x1080; 60p  ->  1080 60p Hq
```

D7200 的菜单字体没有大写 `Q` 字形，`HQ` 会显示成占位符；小写 `q` 在
`Movie quality` 等标签里存在，所以用 `Hq`。

### 校验与重封包

- `nikon_movie_patch.py` 先读 stock，核对表项/标签，再写；
- 写完检查差异只落在声明的 rate/label 范围；
- `repack_firmware.py` 重建目录、模块 CRC、包 CRC，重加密，并用
  `validate_firmware()` 自校验；
- 对 packaging B 的 stale header digest 默认拒绝，避免产生看似有效但会被
  相机拒绝的镜像。

## 安装

- Python 3.9+
- NumPy：`python -m pip install -r requirements.txt`
- 不包含固件和密钥；`key_all.json` 放 `keys/`（已 gitignore）或用 `--key` 指定。

## 用法

完整说明见 [docs/USAGE.md](docs/USAGE.md)，常见问题见
[docs/FAQ.md](docs/FAQ.md)，变更记录见 [CHANGELOG.md](CHANGELOG.md)。最小流程：

1. `tools/decrypt_dslr2.py` 解密原厂镜像，得到 `*.dec.modules/`；
2. `nikon_movie_patch.py --check` 校验 profile；
3. `nikon_movie_patch.py --out` 写补丁模块；
4. `tools/repack_firmware.py` 重封包；
5. 再解密输出，确认只有目标模块/字段变化。

## 菜单标签的三个硬约束

1. **同长度**：UTF-16 池连续存放，不能变长；用空格补齐。
2. **字形存在**：相机字体不是完整 Unicode；缺失字符会显示成方框/怪符号。
   D7200 上大写 `Q` 缺失，用小写 `q` 解决。
3. **不要改分隔符/后续字符串**：只替换声明的字节范围，脚本会拒绝越界差异。

## D3400 / packaging B

D3400 的固件头是 32 字节 packaging B，包含 `SHA1(body || K8)`。D3400 的 K8
已于 2026-11-15 恢复为 `AF08FBDBB582B587`，所以：

- D3400 的 **module profile 已做 stock 校验**；
- 完整镜像可用 `repack_firmware.py --k8 <k8.json>` 校验原镜像摘要并重算；
- 不给 `--k8` 时，工具仍会拒绝写出 stale header；`--allow-stale-header`
  只适合 CRC/QEMU 测试；
- 即使摘要正确，也不代表相机接受该镜像；刷机风险仍然存在。

## 项目结构

```text
E4_HQ_VID/
  nikon_movie_patch.py      数据驱动补丁器
  scan_movie_modes.py       只读表/标签扫描器
  profiles/                 各机型 profile
  tools/                    解密 + 重封包工具链
  tests/                    stock 校验/扫描器测试
  docs/                     用法、加机型、FAQ
  SUPPORT.md                EXPEED 4 全机型支持矩阵
  keys/                     key_all.json 放这里（gitignore）
```

## 测试

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

测试只读 stock 模块；缺少某机型模块时自动跳过。D7200 测试还会断言当前补丁
模块的精确 SHA。

## 贡献

欢迎 profile、扫描器改进、文档和测试。开始前请阅读
[CONTRIBUTING.md](CONTRIBUTING.md)。

**不要提交**固件、解密模块、密钥、可刷写镜像、个人信息或任何你没有权利
分发的内容。贡献默认按 GPL-3.0 授权，并使用 DCO 签名。

## 安全

漏洞、密钥泄露、供应链问题请按 [SECURITY.md](SECURITY.md) 私下报告，不要在
公开 issue 里贴密钥或未公开的固件。

## 法律与许可

- 代码和文档：**GPL-3.0**，见 [LICENSE](LICENSE)。
- 第三方工具来源与版权：见 [NOTICE.md](NOTICE.md)。
- 详细法律声明：见 [LEGAL.md](LEGAL.md)。
- 行为准则：见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

再次强调：本仓库不提供固件或密钥；刷机风险、法律合规和保修后果由使用者
自行承担。

## 致谢

- [WonderLantern/nikon-fw-key-tool](https://github.com/WonderLantern/nikon-fw-key-tool)
  的解密/重封包工具链（GPL-3.0）；
- 提供 D7200/D750/D810/D810A/D4S/D5500/D5600/D3400 模块与测试反馈的贡献者；
- 以及所有遵守法律、只在自有设备上做研究的人。
