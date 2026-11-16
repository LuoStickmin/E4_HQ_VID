# EXPEED 4 支持矩阵 / EXPEED 4 Support Matrix

[中文](#中文) · [English](#english)

> 这里的“支持”分等级，不是所有机型都已有 profile。没有 profile 的机型可以
> 用扫描器加，但需要你自己的解密模块和 stock 校验。

## 中文

### 状态定义

| 标记 | 含义 |
| --- | --- |
| ✅ 真机实测 | 有 profile，作者在相机上刷入并确认码率/回放 |
| 🟩 profile / stock 校验 | 有 profile，脚本核对过原厂表项/标签；未真机验证 |
| 🟨 scanner-ready | 没有 profile；可用 `scan_movie_modes.py` 在解密模块上定位表和标签，再写 profile |
| 🟧 待分析 | 有本地样本，但标准 0x1C 表/UTF-16 标签未自动识别；需要人工分析 |
| 🟥 缺数据 | 没有可用的完整固件/模块，无法生成 profile |
| ⛔ 不在范围 | 不是 EXPEED 4，或不是同一套 DSLR 容器/菜单 |

> **只有 D7200 由作者真机实测。** D750/D810/D3400/D4S/D5500/D5600/D810A
> 都只是 stock 校验，不等于已经在相机上验证，更不等于“可安全刷写”。

### EXPEED 4 单反全表

| 机型 | 发布 | Profile | 封装 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- |
| D4S | 2014-02 | `d4s_hq64.json` | A | 🟩 stock 校验 | 1080p60 HQ 64/60 Mbps；未真机验证 |
| D750 | 2014-09 | `d750_hq64.json` | A | 🟩 stock 校验 | 1080p60 HQ 64/60 Mbps；未真机验证 |
| D810 | 2014-06 | `d810_hq64.json` | A（明文样本） | 🟩 stock 校验 | 1080p60 HQ 64/60 Mbps；未真机验证 |
| D810A | 2015-02 | `d810a_hq64.json` | A | 🟩 stock 校验 | 1080p60 HQ 64/60 Mbps；未真机验证 |
| D7200 | 2015-03 | `d7200_hq64.json` | A | ✅ 真机实测 | 1080p60 HQ 64/60 Mbps + `Hq`；码率/回放正常 |
| D5300 | 2013-10 | — | A（本地样本） | 🟧 待分析 | 本地 1.03 样本未找到标准 0x1C 表/UTF-16 标签；布局可能不同 |
| D5500 | 2015-01 | `d5500_hq64.json` | A | 🟩 stock 校验 | 1080p60 HQ 64/60 Mbps；帧尺寸 + 合并式 `Hq` 标签 |
| D5600 | 2016-11 | `d5600_hq64.json` | **B（加密）** | 🟩 stock 校验（模块级） | 1080p60 HQ 64/60 Mbps；K8 已恢复（`6FA0738BE53A7DE7`），完整镜像已做容器层重封包+回读验证，相机接受度未验证 |
| D3300 | 2014-01 | — | A（本地样本） | 🟧 待分析 | 本地 1.02 样本未找到标准 0x1C 表/UTF-16 标签；布局可能不同 |
| D3400 | 2016-08 | `d3400_hq64.json` | **B（加密）** | 🟩 stock 校验（模块级） | 1080p60 HQ 64/60 Mbps；K8 已恢复（`AF08FBDBB582B587`），完整镜像已做容器层重封包+回读验证，相机接受度未验证 |
| D3500 | 2018-08 | — | 未验证 | 🟥 缺数据 | 本地没有完整镜像/模块；需要相机 dump 或完整固件才能做 |

“封装 A/B”以实际样本为准；未验证的机型可能在 A/B 之间不同。A 没有 header
digest；B 的 32 字节头含 `SHA1(body || K8)`，改 body 需要对应机型的 K8
重算摘要（D3400 的 K8 已恢复为 `AF08FBDBB582B587`；D5600 的 K8 已恢复为
`6FA0738BE53A7DE7`；重算不等于相机验签通过）。

### 不在范围

| 系列 | 原因 |
| --- | --- |
| D5 / D500 / D7500 / D850 | EXPEED 5，不是 E4 |
| Z 5 / Z 6 / Z 7 / Z 8 / Z 9 / Z 50 等 | 不同平台和容器 |
| Nikon 1 系列 | 不同平台/菜单结构 |
| Coolpix / KeyMission | 不同平台 |

### 怎么把 🟧/🟥 变成 ✅

1. 用 `tools/decrypt_dslr2.py` 解密该机型的原厂镜像；
2. `python scan_movie_modes.py --module <b...>.bin --model <MODEL>`；
3. 确认电影表基址、1080p60 HQ 表项、EN/ZH 标签偏移和长度；
4. 写 `profiles/<model>_hq64.json`；
5. `--check` 通过后 `--out`，再重封包并回读验证；
6. 真机短录测试码率/回放/时长/过热，再更新本表。

详见 [docs/ADD_MODEL.md](docs/ADD_MODEL.md)。D5300/D3300 有本地样本但标准布局
未识别，需要人工分析；D3500 需要完整固件或相机 dump，不能靠猜偏移。

## English

### Status legend

| Mark | Meaning |
| --- | --- |
| ✅ camera-tested | profile exists; the author flashed it and confirmed bitrate/playback |
| 🟩 profile / stock-checked | profile exists; stock table/labels verified; not camera-tested |
| 🟨 scanner-ready | no profile; use `scan_movie_modes.py` on a decrypted module, then add a profile |
| 🟧 needs analysis | a local sample exists, but the standard 0x1C table/UTF-16 labels were not auto-detected |
| 🟥 missing data | no complete firmware/module is available, so no profile can be generated |
| ⛔ out of scope | not EXPEED 4, or not the same DSLR container/menu |

> **Only D7200 has been camera-tested by the author.** D750/D810/D3400/D4S/D5500/D5600/D810A
> are stock-checked only; that is not the same as “verified safe to flash”.

### All EXPEED 4 DSLRs

| Model | Announced | Profile | Packaging | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| D4S | 2014-02 | `d4s_hq64.json` | A | 🟩 stock-checked | 1080p60 HQ 64/60 Mbps; not camera-tested |
| D750 | 2014-09 | `d750_hq64.json` | A | 🟩 stock-checked | 1080p60 HQ 64/60 Mbps; not camera-tested |
| D810 | 2014-06 | `d810_hq64.json` | A (plaintext sample) | 🟩 stock-checked | 1080p60 HQ 64/60 Mbps; not camera-tested |
| D810A | 2015-02 | `d810a_hq64.json` | A | 🟩 stock-checked | 1080p60 HQ 64/60 Mbps; not camera-tested |
| D7200 | 2015-03 | `d7200_hq64.json` | A | ✅ camera-tested | 1080p60 HQ 64/60 Mbps + `Hq`; bitrate/playback OK |
| D5300 | 2013-10 | — | A (local sample) | 🟧 needs analysis | local 1.03 sample did not expose the standard 0x1C table/UTF-16 labels |
| D5500 | 2015-01 | `d5500_hq64.json` | A | 🟩 stock-checked | 1080p60 HQ 64/60 Mbps; frame-size + combined `Hq` labels |
| D5600 | 2016-11 | `d5600_hq64.json` | **B (encrypted)** | 🟩 stock-checked (module) | 1080p60 HQ 64/60 Mbps; K8 recovered (`6FA0738BE53A7DE7`); full image repack + decrypt round-trip verified, camera acceptance untested |
| D3300 | 2014-01 | — | A (local sample) | 🟧 needs analysis | local 1.02 sample did not expose the standard 0x1C table/UTF-16 labels |
| D3400 | 2016-08 | `d3400_hq64.json` | **B (encrypted)** | 🟩 stock-checked (module) | 1080p60 HQ 64/60 Mbps; K8 recovered (`AF08FBDBB582B587`); full image repack + decrypt round-trip verified, camera acceptance untested |
| D3500 | 2018-08 | — | unverified | 🟥 missing data | no local full image/module; needs a camera dump or complete firmware |

Packaging A/B is per sample; unverified models may differ. A has no header digest.
B has a 32-byte header containing `SHA1(body || K8)`; changing the body requires
the model's K8 to recompute the digest (D3400's K8 is `AF08FBDBB582B587`;
D5600's is `6FA0738BE53A7DE7`; a matching digest still does not prove camera
acceptance).

### Out of scope

| Series | Reason |
| --- | --- |
| D5 / D500 / D7500 / D850 | EXPEED 5, not E4 |
| Z 5 / Z 6 / Z 7 / Z 8 / Z 9 / Z 50 and other Z bodies | different platform and container |
| Nikon 1 | different platform/menu |
| Coolpix / KeyMission | different platform |

### Turning 🟧/🟥 into ✅

1. decrypt the stock image with `tools/decrypt_dslr2.py`;
2. run `python scan_movie_modes.py --module <b...>.bin --model <MODEL>`;
3. confirm the table base, the 1080p60 HQ entry, and the EN/ZH label offsets and lengths;
4. write `profiles/<model>_hq64.json`;
5. run `--check`, then `--out`, repack and decrypt the output to verify;
6. do a short camera test (bitrate, playback, duration, overheating), then update this table.

See [docs/ADD_MODEL.md](docs/ADD_MODEL.md). D5300/D3300 have local samples but
their standard layout was not detected; D3500 needs a complete firmware image or
camera dump. Do not guess offsets.

## 说明 / Notes

- “EXPEED 4”按 Nikon 公开型号资料整理；如果遗漏了某个 E4 机型，请开 issue 补表。
- 同一机型的不同固件版本也可能改变偏移；profile 必须绑定具体版本。
- packaging B 机型只有在拿到该机型的 K8 后才能重算完整镜像摘要；D3400 的 K8
  已恢复，但这仍只是容器一致性，不等于相机接受或可安全刷写。
