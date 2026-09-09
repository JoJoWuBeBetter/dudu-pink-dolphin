# 内置 CSS 变量全表

来源：LAPLACE Chat 官方「引导模版」（<https://laplace.live/chat/templates>）。

> **注意**：官方说明该模版「并没有积极维护，也并不包含全部变量，仅供参考」，最后更新 2024-09-20。下表是可靠的起点，但平台可能新增变量；拿不准时优先改样式而不是猜变量名，或在配置器里载入内置模版看它实际用了什么。

## 命名约定

`--event-{事件类型}-{部件}-{档位}`

- 无后缀或 `-0`：水友（普通用户）
- `-1`：总督
- `-2`：提督
- `-3`：舰长
- `-1` ~ `-6`（SC / 礼物 / MVP）：价格档位，数字越大档位越高

`--event-username-text-*` 用的是 `0/1/2/3`，SC、礼物、MVP 的 `*-text-*` / `*-bg-*` 用的是 `1..6`。

## `.event` 基础变量

| 变量 | 说明 |
|---|---|
| `--event-font-family` | 全局自定义字体，可引用内置 `--font-sans` |
| `--event-message-text` | 弹幕文本颜色 |
| `--event-message-color` | 弹幕文本颜色（可用 `var(--text-color)` 跟随深浅色自动调整） |
| `--event-username-text-0` | 普通用户用户名颜色 |
| `--event-username-text-1` | 总督用户名颜色 |
| `--event-username-text-2` | 提督用户名颜色 |
| `--event-username-text-3` | 舰长用户名颜色 |

## 弹幕 `.event--message`

| 变量 | 说明 |
|---|---|
| `--avatar-size` | 头像尺寸（默认 18px） |
| `--event-danmaku-text` | 弹幕文本色 |
| `--event-danmaku-text-0..3` | 各档位弹幕文本色 |
| `--event-danmaku-bg-0..3` | 各档位弹幕背景色 |
| `--event-danmaku-current-rank-text` | 「榜 n」文本色 |
| `--event-danmaku-current-rank-text-1..3` | 各档位「榜 n」文本色 |
| `--event-danmaku-current-rank-bg-1..3` | 各档位「榜 n」背景色 |
| `--event-danmaku-mod-text` | 房管标识文本色 |
| `--event-danmaku-streamer-text` | 主播标识文本色 |

「榜 n」图标变量定义可在组件簿查看：<https://storybook.laplace.live/>（文档另给出 chromatic 地址 `https://master--60f5c0ae4a7e3f003ba05641.chromatic.com/`）。

## 醒目留言 `.event--superchat`

| 变量 | 说明 |
|---|---|
| `--event-superchat-top-text` | SC 上方文本色 |
| `--event-superchat-top-text-1..6` | 各档位上方文本色 |
| `--event-superchat-top-bg-1..6` | 各档位上方背景色 |
| `--event-superchat-message-text` | SC 正文文本色 |
| `--event-superchat-message-text-1..6` | 各档位正文文本色 |
| `--event-superchat-bg` | SC 整体背景（默认 `transparent`） |
| `--event-superchat-bg-1..6` | 各档位背景色 |

SC 颜色分为上下两部分，需要分别定义背景。

## 礼物 `.event--gift`

| 变量 | 说明 |
|---|---|
| `--event-gift-text` | 礼物事件文本色 |
| `--event-gift-text-1..6` | 高亮礼物各档位文本色 |
| `--event-gift-bg-1..6` | 高亮礼物各档位背景色 |
| `--event-gift-normal-text-1..6` | 普通礼物各档位文本色 |
| `--event-gift-normal-bg-1..6` | 普通礼物各档位背景色（默认 `transparent`） |

## 上舰提示 `.event--toast`

| 变量 | 说明 |
|---|---|
| `--event-toast-text` | 上舰提示文本色 |
| `--event-toast-text-1..3` | 各档位文本色（1 总督 / 2 提督 / 3 舰长） |
| `--event-toast-bg-1..3` | 各档位背景色 |

`.event-show-as--normal` 排除置顶礼物条，`.event-show-as--sticky` 用于置顶礼物条。

## MVP（守护圣法师等）

| 变量 | 说明 |
|---|---|
| `--event-mvp-text` | MVP 文本色 |
| `--event-mvp-text-1..6` | 各档位文本色 |
| `--event-mvp-bg-1..6` | 各档位背景色 |

## 互动

| 变量 | 说明 |
|---|---|
| `--event-interaction-text-enter` | 进入直播间 |
| `--event-interaction-text-follow` | 关注 |
| `--event-interaction-text-share` | 分享 |
| `--event-interaction-text-follow-special` | 特别关注 |
| `--event-interaction-text-follow-mutual` | 互相关注 |

## 系统与禁言

| 变量 | 说明 |
|---|---|
| `--event-system-text` | 系统消息文本色 |
| `--event-user-block-text` | 禁言提示文本色 |
| `--event-user-block-bg` | 禁言提示背景色 |

## 平台级内置变量（只读，直接引用）

| 变量 | 说明 |
|---|---|
| `--font-sans` | 非衬线字体栈 |
| `--text-color` | 跟随深浅色模式自动调整的文本色 |
| `--color-{name}-{50..950}` | SCAS 色盘，Tailwind 命名，见 `color-system.md` |
| `--mix-base` / `--mix-factor` | SCAS 混合基色 / 混合因子 |

## 用法示例

```css
@layer remote-css {
  /* 弹幕专用变量：集中定义在 .event 上，全事件复用 */
  .event {
    --event-font-family: "ZCOOL KuaiLe", var(--font-sans);
    --event-message-color: var(--text-color);
    --event-username-text-0: var(--color-rose-600);
    --event-username-text-1: var(--color-amber-300);
    --event-username-text-2: var(--color-violet-300);
    --event-username-text-3: var(--color-sky-300);
  }

  /* 按档位微调：总督 / 提督 / 舰长 */
  .event--message.guard-level--1 { --event-danmaku-bg-1: color-mix(in hsl, var(--color-red-900) 60%, transparent); }
  .event--message.guard-level--2 { --event-danmaku-bg-2: color-mix(in hsl, var(--color-purple-900) 60%, transparent); }
  .event--message.guard-level--3 { --event-danmaku-bg-3: color-mix(in hsl, var(--color-blue-900) 60%, transparent); }

  /* SC 上下两段分别上色 */
  .event--superchat.event-show-as--normal .top { --event-superchat-top-bg-1: var(--color-rose-500); }
  .event--superchat.event-show-as--normal .message { --event-superchat-bg-1: var(--color-rose-900); }
}
```
