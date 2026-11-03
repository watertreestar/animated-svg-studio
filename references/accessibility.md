# Accessibility and motion safety

## Accessible naming

For meaningful graphics:

```xml
<svg role="img" aria-labelledby="title desc" ...>
  <title id="title">Request routing architecture</title>
  <desc id="desc">Requests enter a router and are distributed to three workers.</desc>
</svg>
```

For decorative graphics, use `aria-hidden="true"` and do not duplicate surrounding text.

## Reduced motion

In web and framework modes, honor `prefers-reduced-motion: reduce`. Use one of these fallbacks:

- stop on the most informative frame;
- shorten movement and preserve state changes;
- replace travel with a crossfade;
- provide a user-visible pause/replay control.

For standalone SMIL, CSS media queries can hide optional moving layers in browsers that honor them, but not every embedding context does. Therefore make the first frame informative.

Mark nonessential layers with `data-motion="optional"` when using the bundled preview template.

## Flashing and vestibular safety

- Never exceed three flashes per second.
- Avoid full-canvas zooming, spinning, or parallax loops.
- Keep large movement slow and predictable.
- Avoid alternating high-contrast fields.

## Text and contrast

- Maintain readable contrast against every animated background state.
- Do not animate text while it must be read.
- Keep essential labels at a practical mobile size; test around 390 px viewport width.
- Do not encode status by color alone; add shape, label, or icon differences.

## Interaction

Use keyboard-accessible HTML controls for web embeds. If an SVG element itself is interactive, give it a role, label, focus behavior, and a visible focus indication.
