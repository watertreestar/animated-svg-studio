# Warm editorial article theme

Use this warm editorial theme by default for technical explainers, architecture diagrams, and article illustrations when the user has not provided a brand system. It is an independently defined palette for Chinese-first editorial graphics.

## Font stack

Use a Chinese-first system stack so labels render naturally on common mobile and desktop devices:

```text
'Noto Sans SC','PingFang SC','Microsoft YaHei',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif
```

For SVG, place `font-family` on the root `<svg>` so text inherits it. Avoid remote web fonts in portable and constrained-publisher modes.

## Core palette

The source article repeatedly uses these colors:

| Token | Hex | Use |
|---|---|---|
| `paper` | `#FBF8F1` | Main illustration background |
| `ink` | `#1E1C19` | Primary text, strong strokes, dark cards |
| `muted` | `#8F887D` | Secondary text and inactive states |
| `accent` | `#CF4436` | Primary emphasis, active flow, alerts |
| `surface` | `#EDE6D8` | Cards, tracks, subtle panels |
| `body` | `#47423B` | Body text and secondary dark shapes |
| `line` | `#D8D0C1` | Borders and connectors |
| `soft-line` | `#D2C9B8` | Quiet dividers and inactive paths |
| `green` | `#5E7F5A` | Success and secondary status |
| `gold` | `#B08A4E` | Tertiary emphasis |
| `white` | `#FFFFFF` | Text on dark cards and raised surfaces |

## Layout character

- Use warm paper as the full-canvas background rather than pure white.
- Favor 6–18 px rounded corners; reserve larger radii for major containers.
- Use dark `ink` cards sparingly to establish hierarchy.
- Keep connector lines thin and quiet until active.
- Use vermilion `accent` for the one most important active state.
- Use muted text for explanations; avoid blue-gray default SaaS palettes.
- Keep shadows minimal or absent. Separation comes from tone, border, and whitespace.

## Typography hierarchy

- Diagram title: 24–28 px, weight 650–700, `ink`.
- Subtitle: 13–15 px, regular, `muted`.
- Node title: 15–18 px, weight 600–650.
- Node metadata: 12–14 px, regular, `muted` or `body`.
- Avoid long paragraphs inside SVG. Wrap externally or use multiple explicit `<text>` lines.

## Animation character

- Prefer deliberate reveals and short 4–8% scale emphasis.
- Use vermilion moving tokens against quiet taupe connectors.
- Dim inactive nodes to roughly 30–45% opacity instead of hiding them completely.
- Leave a reading pause at the end of each loop.
- Avoid neon glows, glassmorphism, heavy gradients, and excessive bounce.

## Minimal SVG setup

```xml
<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 750 520"
  font-family="'Noto Sans SC','PingFang SC','Microsoft YaHei',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
  <rect width="750" height="520" fill="#FBF8F1"/>
</svg>
```
