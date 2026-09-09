# dudu-pink-dolphin

LAPLACE Chat 的粉色弹幕样式，包含自适应正文框、顶部用户名名牌、可爱的中英日字体，以及按舰长等级区分的头像装饰框。

## 文件

- `laplace-message-frame-decorated.css`：完整的 LAPLACE Chat 自定义 CSS
- `assets/bow.png`：左上蝴蝶结
- `assets/necklace.png`：右上珠链
- `assets/candy.png`：右下糖果
- `assets/avatar/base.png`：普通水友头像框
- `assets/avatar/jz.png`：舰长头像框
- `assets/avatar/td.png`：提督头像框
- `assets/avatar/zd.png`：总督头像框

## 使用

在 LAPLACE Chat 的“样式 → 高级 CSS 编辑器”中粘贴 `laplace-message-frame-decorated.css` 的内容，然后复制到 OBS 的自定义 CSS。

CSS 中的图片路径使用相对路径。直接在 LAPLACE Chat 编辑器中使用本地路径时，浏览器或 OBS 可能无法读取仓库文件；要分享给别人或部署远程模板，需要把整个仓库放在能通过 HTTPS 访问的静态文件服务上，并保持 CSS 文件与 `assets/` 目录的相对位置不变。

顶部参数可以调整名牌、头像和正文布局：

```css
--nameplate-scale: 1;
--nameplate-width: 210px;
--avatar-frame-size: 100px;
--avatar-picture-size: 66%;
--avatar-offset-x: 8px;
--avatar-text-gap: 5px;
--avatar-offset-y: 12px;
--nameplate-offset-y: 4px;
--text-space-top: 35px;
--text-space-bottom: 25px;
--text-space-left: 54px;
--text-space-right: 54px;
--text-line-height: 1.45;
```

名字过长时会在名牌中显示省略号。

## 字体

两份样式的正文与用户名均使用荆南圆体（CSS 字体名 `KeinannMaruPOP`），支持简体中文、繁体中文、英文和日文。字体采用 SIL Open Font License 1.1，可免费商用。CSS 通过顶部的 `@import` 从 [ZeoSeven Fonts](https://fonts.zeoseven.com/items/850/) 在线按需加载字体分包，需要网络访问该字体服务；加载失败时使用系统字体。

[字体项目与授权](https://booth.pm/ja/items/7090983)。若自行托管或随项目分发字体文件，应保留对应版本的版权声明及 OFL 许可证。

## 素材说明

图片素材由项目委托方提供，并随本项目保存为本地文件。仓库中的 CSS 不再暴露原始图片地址。
