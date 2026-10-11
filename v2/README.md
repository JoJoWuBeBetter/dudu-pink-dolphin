# 海豚也是豚 V2

V2（1.2.0，r7）独立维护在本目录。仓库根目录的 1.1.10 样式与原素材保留。

## 当前效果

- 浅粉气泡、简洁胶囊铭牌，左上蝴蝶结与右上小猪。
- 气泡右下角梨子已隐藏；素材及调整参数保留，便于恢复。
- 铭牌两端使用 18×24px 梨子剪影：水友浅灰蓝 `#BED2DD`、舰长蓝 `#65B5DE`、提督紫 `#B58AD5`、总督奶油金黄 `#EFCB78`。
- 四档头像框采用粉色圆环与白色线条，提督双星位于右上；昵称统一为暖棕色。
- 正文留白为上 27px、下 18px、左 24px、右 60px；多行使用均衡换行。宽度、字体和挂件参数保留当前调校值。

## 使用

远程模板使用 [`remote.css`](remote.css)，其素材地址指向本仓库的公开 jsDelivr 地址：

```text
https://cdn.jsdelivr.net/gh/JoJoWuBeBetter/dudu-pink-dolphin@main/v2/remote.css
```

在 LAPLACE Chat「样式 → 远程模板」填写此链接。首次发布后 jsDelivr 可能需要时间刷新；需固定版本时，将 CSS 链接和其中素材地址的 `@main` 一起替换为对应提交 SHA。

高级编辑器或 OBS 自定义 CSS 使用 [`editor.css`](editor.css)，其中规则位于 `custom-css` 层。远程模板规则位于 `remote-css` 层。避免同时留着旧的自定义 CSS 覆盖远程模板。

[`dudu-pink-dolphin.css`](dudu-pink-dolphin.css) 是相对路径源码。自行托管时，将 `./assets/` 替换为公开 HTTPS 素材根地址；远程模板服务应返回 UTF-8 `text/css`，并允许 LAPLACE 跨域访问。

## 参数与范围

CSS 顶部提供字号、铭牌尺寸、头像位置、正文留白及挂件大小／位置／旋转参数。末尾的 `--nameplate-pear-color` 按 `.guard-level--3`（舰长）、`--2`（提督）、`--1`（总督）覆盖；未入航海的弹幕使用水友色。

仅定制普通弹幕 `.event--message`；礼物、Super Chat、开通／续费通知等保留平台样式。进入动画受 `.can-motion` 控制，减少动态时关闭动画。字体由 ZeoSeven 在线加载荆南圆体，失败时使用系统字体。

本版已在 LAPLACE 网页预览核对四档头像框、梨子颜色、长昵称与多行内容。OBS 由使用者实测；新的 GitHub/jsDelivr 分发地址需发布后再验证。回退原版可使用仓库根目录样式。

## 发布内容

仅包含正式 CSS 和所引用的 PNG 素材。未纳入私有 COS 域名、存储桶配置、密钥、登录同步参数、本机路径、交接文档或临时预览文件。
