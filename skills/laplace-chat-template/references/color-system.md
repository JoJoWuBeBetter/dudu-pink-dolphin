# 内置配色系统（SCAS 色盘）

## 是什么

LAPLACE Chat 基于 **Kladewind** 与 **OKLCH** 色彩空间提供了 **Scheme-based Color Auto Switching™（简称 SCAS）** 色盘，会根据当前系统配色自动微调整体明度，比硬编码 hex 更符合人眼视觉，也能跟随深浅色模式。

兼容性：仅支持 **Chromium 版本高于 111** 的 Chrome，或 **OBS 版本高于 31** 的推流软件。低于此版本时 `oklch()` / `color-mix()` 相关效果会失效。

## 命名

所有色盘兼容 Tailwind CSS 的配色命名：

```
red orange amber yellow lime green emerald teal cyan sky blue indigo
violet purple fuchsia pink rose gray
```

每族都有 `50 100 200 300 400 500 600 700 800 900 950` 档，变量名形如 `--color-rose-300`。

用法：

```css
@layer remote-css {
  .event--message .message {
    color: var(--color-rose-700);
    background: var(--color-rose-100);
  }
  /* 深色模式下换档位 */
  [data-theme="dark"] .event--message .message {
    color: var(--color-rose-100);
    background: color-mix(in hsl, var(--color-rose-950) 80%, transparent);
  }
}
```

## 参数

| 变量 | 默认 | 说明 |
|---|---|---|
| `--mix-base` | `#fff` | 混合基色 |
| `--mix-factor` | 浅色 100%，深色 75% | 混合因子，即主色与混合基色所占比例中主色占比 |

调低 `--mix-factor` 或换 `--mix-base` 可以整体改变色盘观感，例如深色场景下降低饱和度：

```css
@layer remote-css {
  [data-theme="dark"] {
    --mix-base: #fffdbf;
    --mix-factor: 50%;
  }
  .event {
    --event-toast-bg-1: color-mix(in hsl, var(--color-red-900) 60%, transparent);
    --event-toast-bg-2: color-mix(in hsl, var(--color-purple-900) 60%, transparent);
    --event-toast-bg-3: color-mix(in hsl, var(--color-blue-900) 60%, transparent);
  }
}
```

## 设计建议

1. **先定 4–6 个色值再写 CSS**：一个主色、一个强调色、一个中性文字色、一个背景色，各档位从同一色族的 50/100/300/600/900/950 里取，避免满屏随机颜色。
2. **深浅色都要看**：用 `--color-*-100/300` 做深色文字色、`--color-*-700/900` 做浅色文字色，或者直接用 `var(--text-color)` 让平台自动切换。
3. **对比度**：文字与背景至少 4.5:1。SC 和礼物事件背景常常很饱和，文字优先选同族最浅档或纯白。
4. **透明背景用 `color-mix(..., transparent)`**，不要写 `rgba()` 硬编码色值——它会脱离 SCAS 的自动调光。
5. **旧版本回退**：如果必须支持 OBS ≤ 31，在变量声明后补一条普通 hex/rgb 回退：

```css
.event--message .message {
  background: #ffe6ef;                                  /* 回退 */
  background: color-mix(in hsl, var(--color-rose-100) 80%, transparent);
}
```
