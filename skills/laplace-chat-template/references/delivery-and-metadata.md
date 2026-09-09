# 交付方式、元数据与校验清单

来源：<https://laplace.live/chat/templates>（文档最后更新 2026-09-08）。

## 1. 三种模版载入方式

### 内置模版（云端载入）

开启后从本站云端载入，特性：

- 不需要在 OBS 里粘贴冗长 CSS，样式始终最新
- 云端模版与自定义 CSS 可共存，自定义 CSS 总是覆盖云端载入的样式
- 可解决「主播不会配置样式」「弹幕机更新导致样式失效无法及时更新」的问题
- 可解决个别第三方推流程序（如哔哩哔哩直播姬）无法加载较长自定义 CSS 的问题
- 上线于 2025-04-21

### 远程模版

开启后从给定 URL 拉取 CSS，方便作者远程交付。

- 测试模版：<https://rsrc.laplace.cn/assets/bubble-alt.css>
- 上线于 2025-04-22

### 高级 CSS 编辑器（自定义 CSS 样式）

最传统的方式，写完复制到 OBS：

- 载入内置模版时，完整 CSS 会进入编辑器，可实时预览编辑
- 激活「云端载入」时，编辑器内容为参考样式，可删到只剩需要覆盖的部分，再复制到 OBS 的自定义 CSS 覆盖云端样式
- 编辑器是 VS Code 同款：支持取色器、VS Code 快捷键、`ctrl+/`（Windows）或 `cmd+/`（macOS）注释
- 编辑内容自动保存在本地，刷新页面可恢复

## 2. 模版优先级

从低到高：

1. `@layer template` —— 云端载入（内置模版）
2. `@layer remote-css` —— 远程模版
3. `@layer custom-css` —— 高级 CSS 编辑器（自定义 CSS 样式）

三种方式可同时存在。利用该特性可以：云端载入一款内置模版 → 远程载入基于它二创的样式 → 在自定义 CSS 里再叠加自己的调整。

层叠层用法参考 MDN：<https://developer.mozilla.org/docs/Web/CSS/@layer>。

## 3. 远程模版交付要求（硬性）

1. 提供一个可用的 CSS 文件，能稳定地通过 **HTTPS** 访问。
2. CSS 内容与在配置器里直接编辑的自定义 CSS 相同，**不需要额外格式**。
3. 使用 `@layer remote-css` 层叠层，以更好兼容模版优先级。
4. 文件尺寸 **小于 1024 KB**（图片素材不计算在内）。
5. 放行所有来自 **Cloudflare Workers** 的 IP（一般不用额外设置；需白名单时参考 Cloudflare IP Ranges）。
6. 放行所有来自 `LAPLACE-Chat/* CSS-Preprocessor` 的 User Agent 请求（例如 `LAPLACE-Chat/1.0.1 CSS-Preprocessor`）。
7. CSS 中的图片素材必须 HTTPS 可访问，并放行来自弹幕机的 **CORS** 请求。
8. 推荐使用**境外服务器**存储，放在中国大陆反而可能很慢。

## 4. 模版元数据

在 CSS 文件最上方定义，用于向用户展示模版信息：

```css
/*
@title        必填：模版标题
@author       必填：作者
@description  选填：模版描述
@updated      选填（建议填写）：May 10, 2025, 1:39:30 AM PDT
@version      选填：版本，建议 semver，例如 1.0.0
@thumbnail    选填：预览图，建议 240×192px 的倍数，完整 HTTPS 链接
*/
```

字段顺序不受影响。真实远程模版里还会出现 `@features`（如 `dark-mode, animated`），属于约定俗成的扩展字段，可写但非文档规定。

完整示例：

```css
/*
@title        气泡样式（魔改）
@description  用来测试远程 CSS 的样式
@author       LAPLACE Chat
@updated      May 10, 2025, 7:02:13 AM PDT
@version      1.0.0
@thumbnail    https://rsrc.laplace.cn/assets/chat-templates/thumbnails/laplace.png
*/
/* 引入 Google Fonts 字体，理论上国内可以直接访问 */
/* @import 不要嵌套在 @layer 层叠层内 */
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,600;1,400;1,600&display=swap');

/* 模版本身样式，建议嵌套在 remote-css 层叠层内，可以更好的兼容模版优先级 */
@layer remote-css {
  body { background-color: rgba(0, 0, 0, 0); }
  /* 其他样式 */
}
```

## 5. 鉴权

本站不参与任何鉴权、验证流程。付费模版如需防止无授权使用，需自行实现，可能方案：

- 为不同客户提供不同 URL，例如 `https://example.com/templates/12345.css`
- 为不同客户提供不同验证参数，例如 `...bubble.css?token=1234567890`
- 只放行来自 `LAPLACE-Chat/* CSS-Preprocessor` 的 UA
- 只放行来自 Cloudflare Workers 的 IP

**注意**：所有出现在屏幕上的内容都能通过技术手段复制提取，不要将链接鉴权作为唯一的防盗版措施。

## 6. 缓存策略

- CSS 预处理器最多把模版缓存 **5 分钟**，即最多每 5 分钟请求一次站源。用户量大时可考虑在站源额外增加缓存时间以降低带宽压力；通常 1 万用户以下不需要过多考虑。
- 客户端通过 **ETag** 验证模版是否更新，默认 `Cache-Control` 头为 **30 分钟**。

发布流程建议：改样式 → 更新 `@version` / `@updated` → 等 5 分钟 → 再刷新验证。若必须立刻生效，换 URL 或加查询参数。

## 7. 交付前校验清单

**结构**

- [ ] 所有规则都在 `@layer remote-css`（远程）或 `@layer custom-css`（编辑器）内
- [ ] `@import` 在文件顶部、层之外
- [ ] 远程模版有 `@title` 与 `@author`，`@version` 已随本次修改更新

**交付**

- [ ] 文件 < 1024 KB
- [ ] HTTPS 可访问，站源放行 `LAPLACE-Chat/* CSS-Preprocessor` UA
- [ ] 所有图片为 HTTPS 绝对地址且允许 CORS
- [ ] `body { background-color: rgba(0, 0, 0, 0); }` 存在（OBS 透明底）

**渲染**

- [ ] 深浅色模式都看过（`[data-theme="dark"]`）
- [ ] `.reduced-motion` 下内容完整可读、无布局跳动
- [ ] 长文本、超长用户名、多行弹幕不溢出（省略号/换行正常）
- [ ] 无 hover 依赖
- [ ] 目标 OBS / Chromium 版本满足所用特性（OKLCH 需 Chromium > 111 / OBS > 31）
- [ ] 在线上配置器里实际预览过一次
