# 海豚也是豚 · dudu-pink-dolphin

LAPLACE Chat 的粉色弹幕样式：自适应正文框、顶部用户名名牌、荆南圆体中英日字体，以及按大航海等级切换的头像装饰框。

<p align="center">
  <img src="assets/preview.png" alt="弹幕样式预览" width="520">
</p>

## 特性

| 特性 | 说明 |
| --- | --- |
| 自适应气泡 | 正文框宽度随内容自适应，长文本自动换行；过长的用户名显示省略号 |
| 顶部名牌 | 用户名绑定真实昵称，居中悬浮在气泡上沿 |
| 大航海头像框 | 水友 / 舰长 / 提督 / 总督 四套头像装饰框自动切换 |
| 中英日字体 | 荆南圆体，覆盖简繁中文、英文与日文假名，回退 `Microsoft YaHei` / `Yu Gothic` / `Meiryo` |
| 进入动效 | 弹幕从左滑入并淡入；弹幕过快时平台自动停用动画，保证可读性 |
| 装饰角标 | 左上蝴蝶结、右上珠链、右下糖果 |

## 使用

### 方式一：远程模版（推荐）

把本样式发布到可稳定访问的 HTTPS 静态托管上，然后在 LAPLACE Chat 的「样式 → 远程模版」中填入该地址：

```
https://<你的静态托管域名>/dudu-pink-dolphin.css
```

样式会随版本自动更新，无需手动维护。发布时请把 CSS 里的 `./assets/...` 换成对应的绝对地址。

### 方式二：自定义 CSS

1. 打开 LAPLACE Chat「样式 → 高级 CSS 编辑器」
2. 粘贴 `dudu-pink-dolphin.css` 的内容
3. 复制到 OBS 浏览器源的「自定义 CSS」

> 仓库内的 CSS 使用**相对路径**引用素材，便于本地预览与二次分发。若要在编辑器或 OBS 中直接使用，请把 `./assets/...` 换成可 HTTPS 访问的绝对地址，并保持文件与 `assets/` 的相对位置不变。

## 可调参数

样式顶部集中了布局参数，改这里即可整体调整：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `--bubble-radius` | `32px` | 气泡圆角半径 |
| `--bubble-border` | `9px` | 气泡内描边宽度（内层白底与气泡边缘的间距） |
| `--nameplate-scale` | `1` | 名牌及名字同步缩放（`0.9` 缩小 / `1.1` 放大） |
| `--nameplate-width` | `210px` | 名牌基础宽度，超出显示省略号 |
| `--avatar-frame-size` | `100px` | 头像装饰框尺寸 |
| `--avatar-picture-size` | `66%` | 框内头像直径 |
| `--avatar-offset-x` | `8px` | 头像水平位移（正数向右） |
| `--avatar-text-gap` | `5px` | 头像与正文框间距 |
| `--avatar-offset-y` | `12px` | 头像距本条顶部 |
| `--nameplate-offset-y` | `4px` | 名牌上下偏移（正数向下） |
| `--text-space-top` | `35px` | 正文上方留白 |
| `--text-space-bottom` | `30px` | 正文下方留白 |
| `--text-space-left` | `30px` | 正文左侧留白 |
| `--text-space-right` | `30px` | 正文右侧留白 |
| `--text-line-height` | `1.45` | 多行文字行距（无单位） |

装饰挂件（三个角标均可独立调整位置与大小，偏移量正数向右 / 向下）：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `--bow-size` | `104px` | 蝴蝶结尺寸 |
| `--bow-offset-x` | `-5px` | 蝴蝶结水平偏移 |
| `--bow-offset-y` | `0px` | 蝴蝶结垂直偏移 |
| `--necklace-size` | `105px` | 项链挂件尺寸 |
| `--necklace-offset-x` | `2px` | 项链挂件水平偏移 |
| `--necklace-offset-y` | `8px` | 项链挂件垂直偏移 |
| `--candy-size` | `58px` | 糖果尺寸 |
| `--candy-offset-x` | `0px` | 糖果水平偏移 |
| `--candy-offset-y` | `0px` | 糖果垂直偏移 |

示例：

```css
.event--message > .message {
  --necklace-size: 130px;      /* 项链放大 */
  --necklace-offset-x: -12px;  /* 项链向左 12px */
  --necklace-offset-y: 10px;   /* 项链向下 10px */
  --bow-offset-x: 6px;         /* 蝴蝶结向右 6px */
  --candy-offset-y: -8px;      /* 糖果向上 8px */
}
```

配色：

| 部位 | 取值 |
| --- | --- |
| 弹幕正文 | `var(--color-pink-500, #f6339a)` —— 平台 SCAS 色盘，随配色方案自动调光 |
| 用户名 | `#826b65` —— 四个档位统一 |

## 目录结构

```
.
├── dudu-pink-dolphin.css    # 样式主文件（相对路径版）
└── assets/
    ├── preview.png          # 本 README 的预览图
    ├── bow.png              # 左上蝴蝶结
    ├── necklace.png         # 右上珠链
    ├── candy.png            # 右下糖果
    └── avatar/
        ├── base.png         # 水友
        ├── jz.png           # 舰长
        ├── td.png           # 提督
        └── zd.png           # 总督
```

## 字体

正文与用户名使用 **荆南圆体**（CSS 字体名 `KeinannMaruPOP`），支持简体中文、繁体中文、英文与日文，采用 SIL Open Font License 1.1，可免费商用。

CSS 通过顶部的 `@import` 从 [ZeoSeven Fonts](https://fonts.zeoseven.com/items/850/) 按需加载字体分包，需要能访问该字体服务；加载失败时自动回退到系统字体（`Microsoft YaHei` / `Yu Gothic` / `Meiryo`）。

[字体项目与授权](https://booth.pm/ja/items/7090983) · 若自行托管或随项目分发字体文件，应保留对应版本的版权声明及 OFL 许可证。

## 授权

本项目采用自定义的 [分享协议](LICENSE.md)，**未经作者授权不得商用**：

- ✅ 个人学习、本地预览；在**未开通任何收益渠道**的直播间中使用
- ✅ 原样分享；保留署名与来源前提下的非商业改版
- ❌ **带收益的直播**（打赏、广告分成、会员、带货、赞助等），含录屏、剪辑与切片
- ❌ 售卖、付费分发，以及付费产品 / 付费服务 / 付费代做等商业集成
- ❌ 去除署名、冒名原创、单独挪用 `assets/` 中的图片素材

**特别授权**：B 站主播 [梨安不迷路](https://space.bilibili.com/1900141897) 已获得免费使用授权，可在带收益的直播间中使用本项目。

如需在带收益的直播间使用或用于任何商业场景，请先通过[项目仓库](https://github.com/JoJoWuBeBetter/dudu-pink-dolphin/issues)联系作者取得授权。

## 素材说明

图片素材由项目委托方提供，随本项目保存为本地文件。仓库中的 CSS 不暴露原始图片地址；发布为远程模版时再回填可 HTTPS 访问的绝对地址。

字体为第三方作品，遵循其自身的 OFL 1.1 授权，不受本协议约束。

## 更新记录

| 版本 | 变更 |
| --- | --- |
| 1.0.18 | 微调项链挂件默认尺寸与位置（`105px` / `+2px` / `+8px`） |
| 1.0.16 – 1.0.17 | 蝴蝶结、项链、糖果三个角标支持独立的位置与缩放参数 |
| 1.0.15 | 更新总督头像框 |
| 1.0.10 – 1.0.14 | 用户名配色迭代：先按大航海等级分色，后统一为 `#826b65` |
| 1.0.7 – 1.0.9 | 字体改为荆南圆体（ZeoSeven 在线分包），补充日文回退 |
| 1.0.4 – 1.0.6 | 弹幕正文按大航海等级配色，随后统一为平台 `pink-500` |
| 1.0.3 | 新增弹幕进入动效（左滑 + 淡入） |
| 1.0.0 – 1.0.2 | 首次发布：气泡、名牌、头像框与素材地址回填 |
