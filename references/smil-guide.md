# SMIL and standalone SVG

Use this mode when the artifact must remain a real `.svg`, run without JavaScript, embed in documentation, or survive environments that accept SVG animation elements.

## Core elements

- `<animate>` changes scalar or list-valued attributes such as `opacity`, `fill`, `stroke-dashoffset`, `cx`, and `d` when paths are compatible.
- `<animateTransform>` changes `translate`, `scale`, `rotate`, `skewX`, or `skewY`.
- `<animateMotion>` moves along a path. Prefer a visible or shared path reference when support is known.
- `<set>` makes a discrete change. Plain `<animate calcMode="discrete">` is often easier to synchronize.

## Timeline model

Choose one master duration per scene. Express every beat against that duration:

```xml
<animate
  attributeName="opacity"
  values="0;0;1;1;0"
  keyTimes="0;0.15;0.24;0.88;1"
  dur="6s"
  repeatCount="indefinite"/>
```

For eased interpolation:

```xml
calcMode="spline"
keySplines="0 0 1 1; .16 1 .3 1; 0 0 1 1; .42 0 .58 1"
```

There must be one fewer `keySplines` segment than `values` entries. `keyTimes` and `values` counts must match.

## Transform hygiene

SVG animation replaces the target transform unless `additive="sum"` is used. The safest pattern is nesting:

```xml
<g transform="translate(240 180)">
  <g>
    <!-- artwork -->
    <animateTransform attributeName="transform" type="scale"
      values="1;1.08;1" dur="2s" repeatCount="indefinite"/>
  </g>
</g>
```

The outer group owns layout; the inner group owns motion.

## Common recipes

### Enter, hold, exit

```xml
<animate attributeName="opacity" values="0;0;1;1;0"
  keyTimes="0;.1;.2;.85;1" dur="6s" repeatCount="indefinite"/>
<animateTransform attributeName="transform" type="translate"
  values="0 14;0 14;0 0;0 0;0 14"
  keyTimes="0;.1;.2;.85;1" dur="6s" repeatCount="indefinite"/>
```

### Draw a path

Set `pathLength="1"`, which makes the timing independent of path length:

```xml
<path d="..." pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">
  <animate attributeName="stroke-dashoffset" values="1;0" dur="1.2s" fill="freeze"/>
</path>
```

### Moving token

For maximum portability, animate `cx`/`cy` or a wrapper translation. Use `<animateMotion>` when the path is curved and the target environment is known to support it.

## Interaction

SMIL event values such as `begin="click"` or `begin="button.click"` are not uniformly accepted by sanitizers. For a standalone SVG they can be appropriate. For constrained publishers use the exact rules in `wechat-mode.md`, and provide a noninteractive fallback.

## Limitations

- Safari and Chromium generally support common SMIL, but embedded environments vary.
- SMIL cannot conveniently express complex application state.
- External assets make a standalone SVG less portable.
- Morphing `d` requires matching path command structures.

When these limitations dominate, switch to web mode rather than forcing SMIL.
