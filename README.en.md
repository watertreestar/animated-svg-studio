# Animated SVG Studio

[中文](README.md) · [English](README.en.md)

A portable Agent Skill for designing, generating, validating, previewing, and adapting animated SVGs. It supports OpenCode / OpenChamber, Claude Code, Codex, standalone SVG, the web, React, Vue, constrained rich-text publishers such as WeChat, and static fallback workflows.

## Features

- Generates portable standalone SVG + SMIL with a self-contained HTML preview by default.
- Supports web CSS / JavaScript, React, Vue, and interactive SVG.
- Validates SVG structure, safety, animation, and platform compatibility.
- Includes a conservative optimizer that preserves animation references and timelines.
- Includes 8 semantic themes and 24 Chinese SVG examples.
- Theme conversion changes fonts and semantic colors without unexpectedly redesigning the layout.
- Covers constrained rich-text environments such as WeChat publishing.
- Requires no third-party Python packages.

## Quick start

### Install as an Agent Skill

Copy or link the entire directory into the Skill directory used by your agent:

```text
OpenCode / OpenChamber  .agents/skills/animated-svg-studio/
Claude Code             .claude/skills/animated-svg-studio/
Codex                   .agents/skills/animated-svg-studio/
```

### Validate an SVG

```bash
python scripts/validate_svg.py assets/starter.svg --profile pure-svg
```

Available profiles:

- `web`: permits scripting and web interaction while reporting risky constructs.
- `pure-svg`: rejects scripts and inline event handlers; permits SMIL.
- `wechat`: applies conservative rich-text SVG restrictions.
- `email`: checks for a static, self-contained fallback.

### Build a preview

```bash
python scripts/build_preview.py assets/starter.svg \
  -o starter-preview.html \
  --title "Animated SVG preview"
```

The preview supports responsive display, reduced motion, replay, SVG download, and source copying.

### Apply a theme

```bash
python scripts/apply_theme.py \
  examples/zh/default-theme/智能体双层架构.svg \
  -o output/architecture-clear-tech.svg \
  --theme clear-tech
```

List all themes:

```bash
python scripts/apply_theme.py --list
```

### Inspect compatibility and optimize

```bash
python scripts/inspect_compatibility.py assets/starter.svg
python scripts/optimize_svg.py assets/starter.svg -o starter.min.svg
```

## Built-in themes

| Theme ID | Name | Best for |
|---|---|---|
| `default-editorial` | Warm Editorial (default) | Technical articles, architecture explainers |
| `ink-paper` | Ink Paper | Chinese narrative, knowledge maps, methodology |
| `clear-tech` | Clear Tech | AI, cloud, APIs, SaaS |
| `dark-terminal` | Dark Terminal | Code, agents, logs, monitoring |
| `fresh-green` | Fresh Green | Education, collaboration, growth, sustainability |
| `bold-signal` | Bold Signal | Launches, conclusions, risk, decisions |
| `crimson-conference` | Crimson Conference | Minimal technical talks and conference visuals |
| `orange-blue-architecture` | Orange Blue Architecture | API flows, system architecture, technical proposals |

Theme tokens live in [`assets/themes.json`](assets/themes.json). Selection and semantic role guidance lives in [`references/themes.md`](references/themes.md).

## Examples

Open [`examples/zh/index.html`](examples/zh/index.html) to browse all themed examples.

Every theme contains the same three layouts:

- `智能体双层架构.svg` — two-layer agent architecture
- `文档审批流程.svg` — document approval workflow
- `任务执行状态.svg` — task execution status

This makes it possible to compare typography and color without layout differences. The web-only interactive example is available at [`examples/web/interactive-network.html`](examples/web/interactive-network.html).

Start a local server:

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8765/examples/zh/index.html
```

## Project structure

```text
animated-svg-studio/
├── SKILL.md
├── README.md
├── README.en.md
├── assets/
│   ├── preview-template.html
│   ├── starter.svg
│   └── themes.json
├── scripts/
│   ├── apply_theme.py
│   ├── build_preview.py
│   ├── inspect_compatibility.py
│   ├── optimize_svg.py
│   └── validate_svg.py
├── references/
├── examples/
│   ├── web/
│   └── zh/
└── evals/
```

## Requirements

- Python 3.9+
- No third-party Python dependencies
- A browser is useful for visual verification, but is not required to generate SVGs

## Design and compatibility principles

- Use motion to explain information rather than decorate it.
- Prefer `transform`, `opacity`, and path-stroke animation.
- Keep the first frame and static fallback meaningful.
- Include `<title>` and `<desc>` in explanatory SVGs.
- Validate with the target profile and test real clients before publishing to constrained platforms.
- Do not assume every email client or sanitizer supports animation.

## Acknowledgements and references

This project is an independent implementation and does not include source code, images, logos, or proprietary assets from the pages below. Some theme color and typography directions were informed by these public references:

- WeChat technical article: <https://mp.weixin.qq.com/s/lcIkBMOKHSvkRYELgkduMg>, used during early visual research for the warm editorial theme.
- Mokkapps Slidev Theme: <https://slidev-theme-mokkapps.netlify.app/2>, used for typography and color research for the crimson conference theme.
- BeAPT Presentation: <https://beapt-presentation.netlify.app/7>, used for typography and color research for the orange-blue architecture theme.

All bundled examples are independently redesigned original SVGs. The project does not redistribute animations, background images, or branded assets from those references.
