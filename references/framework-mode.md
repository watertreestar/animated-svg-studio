# React and Vue modes

Use a component when the graphic participates in application state, takes data as props, needs theming, or will appear more than once.

## Shared principles

- Make width responsive and derive height from `viewBox`.
- Expose meaningful props: data, labels, duration, playing state, theme—not every path coordinate.
- Keep animation styling near the component, but follow the host project's conventions.
- Ensure every instance gets unique IDs for gradients, masks, filters, clip paths, and path references.
- Avoid browser globals during server rendering.
- Honor `prefers-reduced-motion` and an explicit `reducedMotion` prop when appropriate.

## React

Use JSX attribute names (`className`, `strokeWidth`, `fillRule`, `clipPath`). Generate a stable prefix with `useId()`:

```tsx
const rawId = useId();
const prefix = rawId.replace(/:/g, '');
const gradientId = `${prefix}-gradient`;

return (
  <svg viewBox="0 0 720 420" role="img" aria-labelledby={`${prefix}-title`}>
    <title id={`${prefix}-title`}>{title}</title>
    <defs><linearGradient id={gradientId}>...</linearGradient></defs>
    <path fill={`url(#${gradientId})`} d="..." />
  </svg>
);
```

Use `useEffect` for WAAPI startup and clean up animations on unmount. Do not put a new `animate()` call in every render.

## Vue

Use standard SVG attribute spelling in templates. Generate an instance prefix once in `setup()`; do not regenerate it reactively. Scope CSS carefully: selectors inside an inline SVG work, but IDs referenced through `url(#id)` must remain stable.

## Component API example

```ts
type AnimatedFlowProps = {
  nodes: Array<{ id: string; label: string }>;
  duration?: number;
  playing?: boolean;
  reducedMotion?: boolean;
  className?: string;
};
```

Keep geometry generation separate from rendering when the diagram is data-driven. This makes layout testable without a browser.
