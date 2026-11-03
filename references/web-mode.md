# Web mode

Use inline SVG in HTML when the animation needs pointer interaction, replay controls, scroll synchronization, live data, or application state.

## Technology selection

- **CSS transitions:** simple hover/focus/state changes.
- **CSS keyframes:** autonomous loops and decorative motion.
- **Web Animations API (WAAPI):** imperative timelines, replay, pause, speed, and sequencing.
- **requestAnimationFrame:** only for continuous physics, drawing, or data-driven updates that WAAPI cannot express.

Avoid adding a third-party motion library unless the project already uses it or the timeline genuinely needs its sequencing/path features.

## Inline SVG versus `<img>`

Use inline SVG when CSS or JavaScript must address internal elements. An SVG loaded through `<img>` is isolated from the parent page.

## CSS example

```css
.flow-token {
  transform-box: fill-box;
  transform-origin: center;
  animation: travel 4s ease-in-out infinite;
}
@keyframes travel {
  0%, 10% { transform: translateX(0); opacity: 0; }
  20% { opacity: 1; }
  85% { opacity: 1; }
  100% { transform: translateX(320px); opacity: 0; }
}
@media (prefers-reduced-motion: reduce) {
  .flow-token { animation: none; opacity: 1; transform: translateX(160px); }
}
```

## WAAPI example

```js
const token = svg.querySelector('.flow-token');
const animation = token.animate(
  [
    { transform: 'translateX(0)', opacity: 0 },
    { opacity: 1, offset: .15 },
    { transform: 'translateX(320px)', opacity: 0 }
  ],
  { duration: 4000, iterations: Infinity, easing: 'ease-in-out' }
);
```

## Interaction requirements

- Make interactive SVG elements keyboard reachable.
- Use real HTML buttons for global controls when embedding in a page.
- Do not rely solely on hover; support focus and touch.
- Keep hit targets at least about 40 CSS pixels where possible.
- Do not put essential information in a transient tooltip only.

## Security

Do not add remote scripts, analytics, tracking pixels, or user-data submission unless explicitly requested. Treat untrusted SVG as active content: scripts, event handlers, external references, and `foreignObject` can carry risk.
