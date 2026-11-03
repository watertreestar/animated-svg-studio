# Theme system

The skill includes eight coordinated themes. The warm article appearance remains the default.

| ID | 中文名称 | Best for |
|---|---|---|
| `default-editorial` | 暖色编辑 | Technical articles, WeChat explainers, architecture diagrams |
| `ink-paper` | 水墨纸张 | Chinese narrative, methodology, history, knowledge maps |
| `clear-tech` | 清透科技 | AI, cloud, API, SaaS, product architecture |
| `dark-terminal` | 暗色终端 | Code, agents, tools, logs, monitoring, developer demos |
| `fresh-green` | 自然生长 | Education, collaboration, growth, sustainability |
| `bold-signal` | 强信号 | Launches, conclusions, risk, decision and comparison |
| `crimson-conference` | 暗红大会 | Developer conferences, technical talks, agendas, architecture launches |
| `orange-blue-architecture` | 橙蓝架构 | Clean system architecture, API flows, platform diagrams, technical presentations |

Exact tokens are stored in `assets/themes.json`.

## Selection

Use `default-editorial` when the user does not specify a theme. Infer another theme only when the content strongly suggests it:

- terminal, code execution, logs → `dark-terminal`
- cloud, API, software platform → `clear-tech`
- learning, team growth, ecology → `fresh-green`
- urgent comparison, risk, launch → `bold-signal`
- cultural or reflective Chinese content → `ink-paper`
- developer conference, keynote, agenda, stage visual → `crimson-conference`
- clean API architecture, white technical deck, orange/blue system diagram → `orange-blue-architecture`

If the user supplies brand colors, create a custom token set rather than forcing the nearest built-in theme.

## Token roles

Every theme defines `paper`, `ink`, `muted`, `accent`, `surface`, `body`, `line`, `softLine`, `secondary`, `tertiary`, and `white`. Preserve these semantic roles across the canvas, typography, cards, connectors, active states, and data series. Do not merely change the background.

## Applying a theme

```bash
python scripts/apply_theme.py input.svg -o output.svg --theme clear-tech
```

The script replaces exact colors from the default theme and known warm-surface variants used by the bundled examples. It does not recolor raster images, gradients with unrelated colors, or arbitrary user artwork. For a new SVG, generate directly with the selected tokens whenever possible.

After applying `dark-terminal`, visually inspect contrast because legacy examples may use the same default token for both text and filled cards.

## Crimson conference composition

`crimson-conference` is an original palette informed by the user-supplied Mokkapps Slidev reference, not a reproduction of its content or identity. It is a visual skin for the standard diagram layout, not a separate composition. Use a plain light-gray-white canvas, near-black text, deep wine-red accents, and restrained pale-red surfaces. Favor:

- the same geometry, spacing, cards, connectors, hierarchy, and timeline as the selected base example;
- near-black titles and body text;
- dark red reserved for active flow and primary emphasis;
- light gray-white canvas and very pale red-gray surfaces;
- Open Sans-like sans-serif typography, with Chinese system-font fallbacks;
- simple fades and restrained path movement already present in the base composition.

Avoid third-party logos, event marks, mascot silhouettes, proprietary typefaces, and copied text. Do not rearrange the diagram merely to apply this theme. Preserve the base layout unless the user explicitly asks for a new composition.

## Orange-blue architecture palette

`orange-blue-architecture` is informed by the user-supplied BeAPT Slidev reference. Preserve the selected example's layout and use only its general visual system:

- pure white canvas;
- Poppins-like sans-serif typography with Chinese fallbacks;
- near-black headings and dark gray body text;
- bright orange for primary active flow;
- deep navy for secondary emphasis;
- cyan only as a small third accent;
- blue-gray connectors and thin light-gray borders;
- flat or near-flat surfaces without decorative shadows.

Do not copy the reference slide's logos, product names, navigation marks, or exact architecture arrangement.
