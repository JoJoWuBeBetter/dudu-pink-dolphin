---
name: laplace-chat-template
description: 生成、修改、校验和交付 LAPLACE Chat 弹幕模版（自定义 CSS / 远程模版 / 云端内置模版覆盖）。覆盖 @layer 优先级规范、远程模版元数据与交付要求、SCAS 内置色盘与全部内置 CSS 变量、事件 DOM 选择器与 guard-level / event-price-rank 规则、can-motion 与 reduced-motion 动效控制、OBS 透明背景与兼容性边界。当用户要求做 LAPLACE Chat 弹幕样式、气泡框、用户名名牌、头像框、礼物/醒目留言/上舰提示样式、远程模版 CSS、或检查修复已有模版时使用。
license: MIT
metadata:
  source: https://laplace.live/chat/templates
  source-updated: 2026-09-08
  version: "1.0.0"
---

# LAPLACE Chat 模版生成

为 LAPLACE Chat（`laplace.live/chat`，OBS 弹幕浏览器源）生成可直接交付的 CSS 模版。产出物是一份 CSS 文件：要么粘贴进「样式 → 高级 CSS 编辑器」，要么托管到 HTTPS 作为远程模版。

## 何时使用

- 设计/生成新的 LAPLACE Chat 弹幕样式（气泡、名牌、头像框、事件配色）
- 交付远程模版（含元数据头、托管要求）
- 修改或修复已有模版（变量失效、层序冲突、OBS 里不显示、动画不播放）
- 为礼物 / 醒目留言（SC）/ 上舰提示 / 系统消息做定制

不适用于：OBS 场景搭建、弹幕机账号配置、非 LAPLACE 的弹幕工具。

## 三种交付形态（先选形态，再写 CSS）

| 形态 | 层叠层 | 适用 |
|---|---|---|
| 云端载入（内置模版） | `@layer template` | 平台内置，不可编辑；你的 CSS 覆盖它 |
| 远程模版 | `@layer remote-css` | 第三方作者交付，URL 拉取 |
| 高级 CSS 编辑器 | `@layer custom-css` | 主播/开发者自己写，优先级最高 |

优先级从低到高：`template` < `remote-css` < `custom-css`。三者可同时存在，自定义 CSS 永远覆盖远程模版，远程模版永远覆盖云端内置。**写样式时必须放进对应的层**，裸规则（不在任何 `@layer` 内）优先级不可控，是失效的头号原因。

## 工作流

### Step 0：澄清需求（缺信息就问，别猜）

至少要确认：

1. **交付形态**：远程模版（要托管 + 元数据）还是编辑器自定义 CSS？
2. **覆盖范围**：只改弹幕？还是礼物/SC/上舰/系统消息一起？是否包含深色模式？
3. **视觉方向**：配色（可指定主题色，或用 SCAS 色盘变量）、字体、圆角/描边/阴影、是否有 PNG/SVG 素材（蝴蝶结、挂饰、头像框等）。
4. **动效**：要不要入场动画？能不能接受 reduced-motion 下无动画？
5. **素材来源**：用户提供本地图，还是需要占位/纯 CSS 绘制？

如果用户给的是「照着某张图做」或已有项目，先读现有 CSS 与素材，沿用它的变量命名和层叠层。

### Step 1：定层与骨架

- 远程模版 → `@layer remote-css`，必须带元数据头（见 Step 2）。
- 编辑器自定义 → `@layer custom-css`。
- 只覆盖云端内置模版的少数字段 → 仍用 `@layer custom-css`，内容尽量精简（只写覆盖项）。

可选但安全：在 `@import` 之后加一行 `@layer template, remote-css, custom-css;` 把层序钉死。

### Step 2：元数据头（远程模版必填）

放在 CSS 最上方，`@title` 和 `@author` 必填：

```css
/*
@title        气泡样式（魔改）
@author       你的名字
@description  一句话描述
@updated      May 10, 2025, 7:02:13 AM PDT
@version      1.0.0
@thumbnail    https://example.com/thumb.png
@features     dark-mode, animated
*/
```

`@thumbnail` 建议 240×192 的倍数、完整 HTTPS 链接。`@version` 用 semver。字段顺序不限。详见 `references/delivery-and-metadata.md`。

### Step 3：先定设计令牌，再写选择器

在 `.event` 或 `.event--message` 上集中定义变量，再让各事件复用：

```css
@layer remote-css {
  .event {
    --event-font-family: "Jost", var(--font-sans);
    --event-username-text-1: var(--color-rose-300);
    --event-username-text-2: var(--color-fuchsia-300);
    --event-username-text-3: var(--color-sky-300);
  }
}
```

优先用平台内置变量（`--color-*` SCAS 色盘、`--font-sans`、`--text-color`）而不是硬编码色值——它们会跟随深浅色模式自动调整。变量全表见 `references/css-variables.md`，色盘见 `references/color-system.md`。

### Step 4：变量覆盖优先，DOM 改造其次

按代价从低到高：

1. **改内置变量**（颜色、字体）——最稳，跨版本兼容。
2. **给类加样式**（`.event--message .message` 改内边距、圆角、背景）。
3. **改布局**（grid/flex 重排 `.event--message`，`.meta { display: contents }` 让头像和名牌脱出原容器）。
4. **加装饰层**（`::before` / `::after` 挂 PNG，配合 `isolation: isolate` 和 `overflow: visible`）。
5. **隐藏平台元素**（`.mod-badge`、`.guard-badge`、`.current-rank`、`.avatar-alt-*` 等）。

DOM 结构与选择器地图见 `references/dom-selectors.md`。写覆盖样式时通常需要 `!important`（平台样式优先级高），但要把选择器限定到具体事件，不要全局滥用。

### Step 5：动效必须挂在 `.can-motion` 下

平台会按弹幕速率在事件列表上切换 `.can-motion` / `.reduced-motion`；控制台模式恒为 `reduced-motion`。所以：

```css
@layer remote-css {
  .event--message {
    /* 只对最后 n+2 条弹幕加动画，避免长列表持续动画 */
    .can-motion & :nth-last-child(-n + 2) {
      animation: slide-in ease-out forwards;
      animation-duration: var(--animation-duration);
    }
  }
  @keyframes slide-in { from { opacity: 0; transform: translateX(-8px); } }
}
```

硬性要求：`reduced-motion` 下内容必须完整可读（不能靠动画才能看见），不要在动画里做布局性变化。

### Step 6：OBS 透明背景

OBS 浏览器源需要透明底，模版里补上：

```css
@layer remote-css {
  body { background-color: rgba(0, 0, 0, 0); }
}
```

### Step 7：素材

- 远程模版里的图片**必须** HTTPS 可访问，并放行弹幕机的 CORS 请求；相对路径只在「CSS 与 assets 同源托管」时有效。
- 交付给别人时，把 CSS 与 `assets/` 一起托管，保持相对位置不变；推荐境外服务器（国内存储反而慢）。
- 单文件 CSS 小于 1024 KB（图片不算）。
- 大 PNG 先用工具压一压；能用 CSS 画就别用图。

### Step 8：校验（交付前必做）

```bash
python3 scripts/validate_template.py path/to/template.css --mode remote
```

`--mode remote` 检查元数据、层、HTTPS、体积；`--mode editor` 只检查层与兼容性；`--mode auto` 自动判断。脚本退出码非 0 表示有阻断问题。

还要人工过一遍 `references/delivery-and-metadata.md` 末尾的交付清单。

### Step 9：本地预览（可选，强烈建议）

`templates/preview.html` 是 LAPLACE 事件 DOM 的本地仿真页，改 CSS 后刷新即可看效果，比反复刷新线上配置页快得多。它的基础样式放在 `@layer template`，因此候选模版的 `remote-css` / `custom-css` 会按文档规定的优先级覆盖它。

```bash
# 在技能目录下起一个静态服务器（相对路径才不会踩 file:// 的坑）
python3 -m http.server 8080
# 浏览器打开 http://127.0.0.1:8080/templates/preview.html
```

`templates/probe-styles.html` 是同一套 DOM 的「计算样式探针」，把结果以 JSON 打到页面上，适合无法看截图时做自动化验证：

```bash
# ?css= 相对于服务器根目录，默认 remote-template.css
python3 -m http.server 8080
# http://127.0.0.1:8080/templates/probe-styles.html?css=../../your-template.css

# 有 Chrome 时可直接取回结果
chrome --headless=new --dump-dom \
  "http://127.0.0.1:8080/templates/probe-styles.html?css=../../your-template.css" \
  | python3 -c "import sys,re,html;d=sys.stdin.read();m=re.search(r'<pre id=\"out\">(.*?)</pre>',d,re.S);print(html.unescape(m.group(1)))"
```

重点看：`sheets` 里出现 `CSSLayerBlockRule`（层被正确解析）、`body_bg` 为透明、`message_radius`/`message_padding`/`message_bg` 与设计一致、深色模式下 `border`/`bg` 有变化、`animation_name` 只在预期位置出现。

预览是近似还原（色盘用 hex、结构为简化模拟），最终仍要在线上配置器里确认一次。

### Step 10：交付说明

给用户的交付内容里写清楚：粘贴位置（高级 CSS 编辑器 / OBS 自定义 CSS）、是否依赖远程素材、深浅色模式表现、以及需要对方做的托管步骤（若为远程模版）。

## 硬性规则

1. 所有样式必须在 `@layer remote-css` 或 `@layer custom-css` 内，不能裸写。
2. `@import` 不能嵌套在 `@layer` 内（放在文件顶部、层之外）。
3. 远程模版必须：HTTPS 稳定访问、`@title`/`@author` 元数据、< 1024 KB、放行 `LAPLACE-Chat/* CSS-Preprocessor` UA 与 Cloudflare Workers IP。
4. 图片素材必须 HTTPS + CORS；不要交付 `./assets/...` 相对路径给远程模版。
5. 动效必须包在 `.can-motion` 下，`.reduced-motion` 下保持可读。
6. OKLCH 色盘需要 Chromium > 111 / OBS > 31；更新的特性（`text-wrap: pretty`、`@scope`、`light-dark()`、`anchor()`）要么不用，要么给回退。
7. 深色模式用 `[data-theme="dark"]` 选择器，不要用 `@media (prefers-color-scheme: dark)`。
8. 不要依赖 hover / 鼠标交互，OBS 浏览器源没有指针。
9. 改内置模版前先读它的变量用法，沿用命名，别另起一套。
10. 交付前跑校验脚本。

## 参考资料

| 文件 | 内容 |
|---|---|
| `references/delivery-and-metadata.md` | 三种载入方式、优先级、远程交付要求、元数据规范、鉴权、缓存、交付清单 |
| `references/css-variables.md` | 全部内置 CSS 变量（弹幕/SC/礼物/上舰/MVP/互动/系统/禁言） |
| `references/dom-selectors.md` | 事件 DOM 结构、选择器地图、guard-level / event-price-rank / 事件修饰类 |
| `references/color-system.md` | SCAS 色盘、Tailwind 命名、`--mix-base` / `--mix-factor`、兼容性 |
| `templates/remote-template.css` | 远程模版骨架（含元数据 + 层 + 令牌 + 动效） |
| `templates/custom-css-snippet.css` | 编辑器自定义 CSS 精简覆盖骨架 |
| `templates/preview.html` | 本地预览仿真页 |
| `templates/probe-styles.html` | 计算样式探针（可自动化验证） |
| `scripts/validate_template.py` | 静态校验脚本 |

## 常见坑

- **样式没生效**：多半是裸规则或层用错；远程模版必须 `remote-css`，编辑器必须 `custom-css`。
- **改了远程模版看不到更新**：预处理器最多缓存 5 分钟，客户端 ETag 校验、默认 `Cache-Control` 30 分钟。改完先等 5 分钟，或换 URL / 加版本参数。
- **字体没加载**：`@import` 被放进了 `@layer` 里，或者排在其它规则之后。
- **头像/名牌错位**：`.meta` 是 flex 容器，用 `.meta { display: contents }` 把它「拆掉」再自己 grid 排。
- **装饰图被裁掉**：父级 `overflow: hidden`；给容器 `overflow: visible` 并让装饰层用 `inset` 负值外扩。
- **OBS 里背景是黑的**：忘了 `body { background-color: rgba(0,0,0,0); }`。
- **动画在弹幕多时卡住**：没挂 `.can-motion`，或对全部事件而非最后几条做动画。
- **深色模式颜色不对**：硬编码了浅色值；改用 `--color-*` 或 `[data-theme="dark"]` 覆盖。
