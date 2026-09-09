# 事件 DOM 结构与选择器地图

选择器来自官方「引导模版」与仓库中已在真实环境使用的模版（`laplace-message-frame-decorated.css`）。

> 平台 DOM 会随版本演进。写样式前若不确定，先在线上配置器里对元素右键 → 检查，或用组件簿 <https://storybook.laplace.live/> 对照。**优先用变量覆盖**，只有变量覆盖不到时才动 DOM。

## 1. 结构总览

```
.event
├── .event--message                    弹幕
│   ├── .meta                          flex 容器（头像 + 用户名）
│   │   ├── .sender-avatar
│   │   │   ├── .avatar-img-wrap > img.avatar
│   │   │   └── .avatar-frame          头像装饰框层
│   │   └── .username
│   │       └── .username-text         真实用户名文本
│   ├── .message                       正文（气泡本体）
│   ├── .fans-medal
│   │   ├── .fans-medal-content        勋章名
│   │   └── .fans-medal-level          勋章等级
│   ├── .current-rank                  「榜 n」图标
│   ├── .mod-badge                     房管图标
│   ├── .guard-badge                   舰长图标
│   └── .avatar-alt-outer / .avatar-alt-top / .avatar-alt-bottom
├── .event--gift                       礼物
├── .event--superchat                  醒目留言
│   ├── .top                           上方（金额/用户名区）
│   └── .message                       下方正文
├── .event--toast                      上舰提示 / 置顶礼物条
└── .event--system                     系统消息
```

## 2. 修饰类

| 类 | 含义 |
|---|---|
| `.guard-level--1` | 总督 |
| `.guard-level--2` | 提督 |
| `.guard-level--3` | 舰长 |
| （无 guard-level 类） | 水友 |
| `.event-show-as--normal` | 排除置顶礼物条 |
| `.event-show-as--sticky` | 置顶礼物条 |
| `.event-size--highlight` | 排除非高亮礼物事件 |
| `.event-size--normal` | 非高亮事件 |
| `.event-price-rank--1..6` | 按价格档位统一命中礼物与 SC |
| `.event-superchat-rank--{n}` | 只命中 SC 的价格档位 |
| `.event-gift-rank--{n}` | 只命中礼物的价格档位 |
| `.can-motion` | 事件速率低于阈值时应用（列表根节点） |
| `.reduced-motion` | 事件速率高于阈值时应用；控制台模式恒为它 |

组合示例（来自官方引导模版）：

```css
/* 上舰 / 置顶礼物条 */
.event--toast.event-show-as--normal { }

/* 高亮礼物 */
.event--gift.event-show-as--normal.event-size--highlight { }

/* SC 与正文 */
.event--superchat.event-show-as--normal { }
.event--superchat.event-show-as--normal .top { }
.event--superchat.event-show-as--normal .message { }

/* 统一按价格档位 */
.event .event-price-rank--1 { }
.event .event-price-rank--2 { }
```

## 3. 改布局的常用手法

`.event--message` 默认是 flex，`.meta` 与 `.message` 是兄弟。想把头像放到左侧、正文放到右侧并让名牌骑在气泡上沿，标准做法是「拆掉 `.meta` 再自己排 grid」：

```css
@layer custom-css {
  .event--message {
    display: grid !important;
    grid-template-columns: var(--avatar-frame-size) minmax(0, 1fr);
    column-gap: var(--avatar-text-gap);
    position: relative;
    width: 100%;
    box-sizing: border-box;
    padding: 0 !important;
  }
  /* 让 .meta 不再参与布局，其子元素直接成为 grid 子项 */
  .event--message > .meta { display: contents !important; }
  .event--message > .message { grid-column: 2; grid-row: 1; }
  .event--message > .meta > .sender-avatar { grid-column: 1; grid-row: 1; align-self: start; }
  /* 名牌绝对定位到气泡上沿中央 */
  .event--message > .meta > .username {
    position: absolute !important;
    top: calc(7px + var(--nameplate-offset-y));
    left: calc((100% + var(--avatar-frame-size) + var(--avatar-text-gap)) / 2);
    transform: translateX(-50%) scale(var(--nameplate-scale));
    transform-origin: center;
  }
}
```

要点：

- 平台样式优先级高，覆盖必须 `!important`，且选择器要精确到 `.event--message > .meta > .username` 这种层级。
- 头像框用 `background: var(--custom-avatar-frame) center / contain no-repeat` 铺在 `.avatar-frame` 上，头像本体 `.avatar-img-wrap` 用百分比居中缩小，二者叠放用 `z-index` 分层。
- 装饰图挂在 `.message::before`，用负 `inset` 外扩，容器加 `isolation: isolate`、`overflow: visible`，避免被裁切。
- 隐藏平台元素：`.mod-badge`、`.guard-badge`、`.current-rank`、`.avatar-alt-*`，以及 `.meta` 下除头像和用户名之外的子元素。

## 4. 按档位换素材

```css
@layer custom-css {
  .event--message { --custom-avatar-frame: url("./assets/avatar/base.png"); }
  .event--message.guard-level--3 { --custom-avatar-frame: url("./assets/avatar/jz.png"); } /* 舰长 */
  .event--message.guard-level--2 { --custom-avatar-frame: url("./assets/avatar/td.png"); } /* 提督 */
  .event--message.guard-level--1 { --custom-avatar-frame: url("./assets/avatar/zd.png"); } /* 总督 */
}
```

远程模版里把相对路径换成 HTTPS 绝对地址。

## 5. 动效控制

```css
@layer remote-css {
  .event--message {
    /* 只对最后 n+2 条弹幕加动画 */
    .can-motion & :nth-last-child(-n + 2) {
      animation: slideInFromBar1 ease-out forwards;
      animation-duration: var(--animation-duration);
    }
  }
  @keyframes slideInFromBar1 {
    from { opacity: 0; transform: translateX(-12px); }
    to   { opacity: 1; transform: none; }
  }
}
```

- 条件类名由平台按事件速率自动切换，不要自己加。
- 控制台模式恒为 `.reduced-motion`，所以动画只能是增强，不能是信息载体。
- 用 `:nth-last-child(-n + 2)` 之类限制作用范围，否则长列表会持续重排。

**两种写法的区别**（容易搞混）：

```css
/* A. 官方引导模版的写法：编译为 .can-motion .event--message :nth-last-child(-n + 2)
      命中的是「事件内部」最后两个子元素 */
.event--message { .can-motion & :nth-last-child(-n + 2) { } }

/* B. 想只给「最后几条事件」加动画，把伪类挂在事件本身上：
      编译为 .can-motion .event--message:nth-last-child(-n + 2) */
.can-motion .event--message:nth-last-child(-n + 2) { }
```

官方文档给出的片段是 A；如果你的目标是「最后 n 条弹幕才动」，用 B。两者都要求动画在 `.reduced-motion` 下退化为无动画且内容可读。

## 6. 可选增强（注意兼容性）

这些写法能提升观感，但需要高于基线的 Chromium，且属于「不支持就静默忽略」，可安全附带：

```css
.event--message .message {
  text-wrap: pretty;        /* Chromium 117+，中文长句换行更均匀 */
  overflow-wrap: anywhere;  /* 兜底，防长英文/URL 撑破气泡 */
}
```

基线内的写法（Chromium 111 / OBS 31 起可用）：`color-mix()`、`oklch()`、`:has()`、`@layer`、CSS 嵌套。

超出基线的写法（需要更高版本，务必确认目标 OBS 版本）：`text-wrap: pretty`（117）、`@starting-style`（117）、`@scope`（118）、`light-dark()`（123）、`anchor()`（125）。
