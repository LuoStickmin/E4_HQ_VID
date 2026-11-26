# E4 movie time limits

EXPEED 4 单反电影时长表的**只读扫描**与**数据补丁**工具。表项是
little-endian u32 毫秒值，不是代码：

| 值 | 含义 |
| ---: | --- |
| 600000 (`0x000927C0`) | 10 min |
| 1200000 (`0x00124F80`) | 20 min |
| 1799000 (`0x001B7358`) | 29:59 |
| 3599000 (`0x0036EA98`) | 59:59 |

Nikon-Patch 的 **D810 1.14 “Remove Time Based Video Restrictions”** 补丁就是改
同类值（`1200000`/`1799000` → `0x05CB2780`，约 27 小时），说明这是 E4 上已经
被走过的数据层路径。

## 支持的机型

| 机型 | 模块 | 表偏移 | 项数 | Profile |
| --- | --- | ---: | ---: | --- |
| D750 1.15 | `b1010_115a.bin` | `0x2F2104` | 30 | `profiles/d750_0115_time59.json` |
| D7200 1.04 | `b1230_104.bin` | `0x2DDD98` | 30 | `profiles/d7200_0104_time59.json` |

D810 1.14 有 Nikon-Patch 的整包补丁（`0x2BA67C`/`0x2EBBB0`），但那是**容器
偏移**；模块级偏移需用 `scan_time_tables.py` 在 `b920_114.bin` 上重新确认。
D3300 1.02 的同类常量在 `0x1897D8`/`0x189CA4`，更像代码内常量，不是这张 30 项
表，需单独分析。

各档原厂单段上限与 8/16/32/64 GB 卡累计时长见
[docs/CARD_TIMES.md](docs/CARD_TIMES.md)；4 GB/59:59 的单段表见
[docs/MAX_DURATIONS.md](docs/MAX_DURATIONS.md)。

## 用法

```powershell
# 1. 只检查 stock 表（不写文件）
python time_limits\time_limit_patch.py --module b1230_104.bin `
  --profile time_limits\profiles\d7200_0104_time59.json --check

# 2. 写补丁模块（30 项全 3599000 ms）
python time_limits\time_limit_patch.py --module b1230_104.bin `
  --profile time_limits\profiles\d7200_0104_time59.json `
  --out b1230_104.time59.bin --json report.json
```

补丁只改 30 个 u32，实际变化 90 字节（每个 u32 的高字节本来就是 `0x00`），
范围 `0x2DDD98..0x2DDE0F`，表外 0 字节。

然后按主仓库流程重封包：

```powershell
python tools\repack_firmware.py --key keys\key_all.json `
  --firmware D7200_0104.bin `
  --replace-module b1230_104.bin=b1230_104.time59.bin `
  --keep-tags --out D7200_0104.time59.bin
```

## D7200 50p / 60p 都是 64/60

主仓库的 `d7200_hq64.json` 只改 1080p60 HQ。`profiles/d7200_hq64_50p.json`
把 **60p 和 50p 的 HQ 行**都改成 64/60，并替换 60p/50p 标签：

```powershell
python nikon_movie_patch.py `
  --module b1230_104.bin `
  --config time_limits\profiles\d7200_hq64_50p.json `
  --out b1230_104.hq64_50p.bin

python time_limits\time_limit_patch.py `
  --module b1230_104.hq64_50p.bin `
  --profile time_limits\profiles\d7200_0104_time59.json `
  --out b1230_104.hq64_50p.time59.bin
```

再按上面的 `repack_firmware.py` 命令替换 `b1230_104.bin`。

已验证：这个流程生成的模块 SHA-256 为
`395d707ad0e8df319ac58f2cc5aa74b76403b758eac642afdfe30e29457849c3`，
与本地构建的镜像一致；重封包后的镜像 SHA-256 为
`93974982a0c89cdc7876d005a65f880eaecae09a5fa44f2a5b707a94c305288b`
（镜像不随仓库分发）。

## 重要限制

- **时长表不解除 4 GB 单文件上限。** D7200 实测封口在约 `0xFC000000`
  （4 GiB − 64 MiB，4,227,858,432 B）：64 Mbps 约 8:48，42 Mbps 约 13:25，
  24 Mbps 约 23:29，≤9.4 Mbps 才可能 59:59。
- **相机回放还依赖 `udta/NCDT`。** 长文件写不出 `NCDT` 时，相机报
  “无法显示该文件”，通用播放器正常；详见 [KNOWN_ISSUES.md](../KNOWN_ISSUES.md)
  与 [docs/ANALYSIS_4740_4741.md](docs/ANALYSIS_4740_4741.md)。
- 本仓库不放固件、密钥或可刷镜像；刷机风险自负。

## English

Read-only scanner and data patcher for the EXPEED 4 movie time-limit table
(u32 milliseconds). D750 1.15 (`0x2F2104`) and D7200 1.04 (`0x2DDD98`) are
mapped. The D7200 `d7200_hq64_50p.json` profile raises both 1080p60 and
1080p50 HQ to 64/60 Mbps. The time table does **not** lift the ~4 GB per-file
cap or the camera's `NCDT` playback requirement; see the known-issues doc.
