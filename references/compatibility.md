# Compatibility and fallback strategy

SVG support depends on both the browser and the embedding mechanism. A feature that works in a standalone browser tab can fail when placed in an `<img>`, email client, CMS sanitizer, PDF converter, or rich-text editor.

## Practical matrix

| Feature | Standalone SVG | Inline web SVG | React/Vue | Rich-text/WeChat | Email |
|---|---|---|---|---|---|
| Basic SVG shapes | Strong | Strong | Strong | Usually strong | Mixed |
| SMIL | Generally good | Generally good | Generally good | Platform-specific | Weak/mixed |
| CSS animation | Context-dependent | Strong | Strong | Often stripped | Weak/mixed |
| JavaScript/WAAPI | Not in `<img>` | Strong | Strong | Usually forbidden | Forbidden |
| `foreignObject` | Mixed | Fair | Fair | Often stripped | Weak |
| External images/fonts | CORS/network dependent | Network dependent | Network dependent | Host restrictions | Client restrictions |
| Filters/masks | Generally good | Good | Good | Test carefully | Mixed |

## Fallback hierarchy

1. Meaningful first SVG frame
2. Static SVG without animation
3. PNG for broad rendering reliability
4. GIF/WebP/video only when motion is essential and the target supports it

## Testing levels

- **Source validation:** XML, references, profiles, safety.
- **Browser preview:** layout, motion, console.
- **Embed test:** the exact HTML/component mechanism.
- **Destination test:** actual CMS, app, email client, or publishing preview.

State which level was completed. Do not conflate a browser preview with a destination-platform test.

## External resources

Data URIs maximize portability but can inflate source size. External assets improve caching and editing but require network access and host permissions. Choose based on the destination and explicitly report the tradeoff.
