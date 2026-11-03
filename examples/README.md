# Animated SVG examples

Examples are organized by language, runtime, and theme instead of being mixed in one directory.

```text
examples/
├── zh/
│   ├── index.html
│   ├── default-theme/
│   ├── ink-paper/
│   ├── clear-tech/
│   ├── dark-terminal/
│   ├── fresh-green/
│   ├── bold-signal/
│   └── crimson-conference/
└── web/
    └── interactive-network.html
```

Each SVG theme directory contains the same three layouts so palettes can be compared without layout changes:

- `智能体双层架构.svg`: Router and parallel Worker flow
- `文档审批流程.svg`: four-stage sequential workflow
- `任务执行状态.svg`: compact processing indicator

Open `zh/index.html` for the complete gallery. Open a theme directory's `index.html` to review only that theme.

The web-only interactive example remains separate because it uses CSS and JavaScript rather than portable SMIL.

## Validate all portable examples

PowerShell:

```powershell
Get-ChildItem examples/zh -Recurse -Filter *.svg | ForEach-Object {
  python scripts/validate_svg.py $_.FullName --profile pure-svg
}
```

## Adaptation guidance

- Start from the theme and layout closest to the request.
- Replace labels before changing geometry.
- Preserve the synchronized master duration.
- Keep `<title>`, `<desc>`, `viewBox`, and a meaningful first frame.
- Run validation after changing IDs, paths, references, or animation timing.
