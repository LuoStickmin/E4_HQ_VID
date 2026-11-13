# FAQ

## 64 Mbps 是 64 MB/s 吗？

不是。`64 Mbps` 是 **64 megabit per second**，约 **8 MB/s**。
`64 Mbps` 录制约 **28.8 GB/小时**；10 秒约 80 MB。

## 为什么只改 HQ 行，Normal 还是 24/20 Mbps？

profile 只改 1080p60 的 **HQ** 表项（`rate_a/rate_b`），Normal 表项保持 stock。
这是刻意的：保留一个低码率档位，也避免误以为 Normal 也变了。

要 Normal 也 64 Mbps，在 profile 里再加一个 `movie_rate` patch，指向同一分辨率的
NQ 表项（例如 D7200 entry 2），把 rates 设为 `[64000000, 60000000]`。

## 为什么菜单显示 `Hq` 而不是 `HQ`？

D7200 的菜单字体没有大写 `Q` 字形，`HQ` 的 `Q` 会变成方框/怪符号。小写 `q` 在
`Movie quality` 等标签里存在，所以用 `Hq`。D3400 同理使用小写 `q`。

## 为什么标签不能直接写 `1920x1080; 60p HQ`？

菜单标签在连续的 UTF-16LE 池里，长度一变，后面的所有标签都会错位。因此必须
**同字符数**替换。本仓库用紧凑写法 `1080 60p Hq`，不足的长度用空格补齐。

## 为什么 640×424 模式会花屏/条纹？

表里有 640×424 记录，但编码器索引 `0x12/0x13` 在 D7200 上会别名到 1080p60，
或者 encoder 仍按 1080p buffer/stride 写。结果是 640×424 容器 + 错误行跨距，
出现规律条纹。强制隔行、去隔行、SPS 改 i 都不能修复；这是编码器 buffer/stride
问题，不是播放器场序问题。仓库不提供 640×424 profile。

## 为什么 D3400 不能直接生成可刷镜像？

D3400 是 **packaging B**：32 字节头包含 `SHA1(body || K8)`。K8 未知，改了 body
就会让 header digest 过期。`repack_firmware.py` 默认拒绝这种镜像；
`--allow-stale-header` 可以绕过，但相机可能拒刷。D3400 的模块级 profile 仍然
可以校验和使用。

## 为什么 stock 校验失败？

常见原因：

- 固件版本不对（例如 D750 1.15 vs 1.14）；
- 模块取错（不是大的 `b*.bin`）；
- profile 表偏移属于另一份固件；
- 文件被解压/修改过；
- 大小端或解密不完整。

**不要**在 stock 校验失败时继续刷写。

## 怎么确认补丁只改了该改的地方？

```bash
python nikon_movie_patch.py --module <stock.bin> \
  --config profiles/<model>_hq64.json --check
```

`--check` 会核对每个 stock 值，然后显示 changed bytes。写完后再用
`cmp`/`git diff --no-index` 或 Python 计算差异；正常 D7200/D750/D810 是 29 B，
D3400 是 69 B。超过这个范围说明 profile 有问题。

## 64 Mbps 会不会过热/卡写不进？

64 Mbps 约 8 MB/s，正常 SD 卡通常足够；但老卡、假卡、长时间录制、高温环境仍
可能出问题。先短录测试，观察是否停录、卡错误、过热警告。不同机型的散热和
编码器限制不同，没有统一的“安全值”。

## 为什么仓库不提供固件和 `key_all.json`？

版权和合规原因。固件版权属于尼康；密钥材料不应随仓库分发。你需要自己合法
取得固件和密钥，放在 `keys/`（已 gitignore）或用 `--key` 指定。

## 支持 D850 / D5 / Z 系列吗？

当前 profile 只覆盖 D7200、D750、D810、D3400。D850/D5 是 packaging B，且
header digest/K8 问题更复杂；Z 系列是不同平台。不要直接套用 EXPEED 4 的偏移。
可以用 `scan_movie_modes.py` 先扫描，但需要自己确认表/标签和封装。

## 可以加 AVI / MP4 录制吗？

不能通过这种表/标签补丁实现。D7200/D750 的录像管线是 MOV/H.264；没有 AVI
muxer 或 MJPEG 编码器。容器格式不是改一个菜单项就能加的。

## 怎么给自己的机型加 profile？

```bash
python scan_movie_modes.py --module <b...>.bin --model <MODEL>
```

确认表偏移、1080p60 HQ 表项、英文/中文标签偏移和长度，写成 JSON，先
`--check`，再 `--out`，最后重封包并回读验证。详见
[ADD_MODEL.md](ADD_MODEL.md)。

## 为什么 README 里 D7200 有精确 SHA，其他机型没有？

D7200 是作者实际刷入并验证的当前状态，所以给出模块和镜像的精确 SHA。
D750/D810/D3400 只做了 stock 校验，没有在相机上验证；不同固件版本/重封包
环境可能产生不同字节，不能给出统一的“已实测”SHA。
