# Animation patterns

Use these as compositional patterns, not rigid templates.

## Recommended pacing

| Pattern | Typical duration | Notes |
|---|---:|---|
| Micro icon | 0.4–1.2 s | Triggered, usually not infinite |
| Status/loading | 0.9–2 s | Gentle repeat |
| Product feature | 3–6 s | One idea per loop |
| Architecture explainer | 5–8 s | Include reading pauses |
| Tutorial sequence | 6–12 s | Consider controls instead of endless loop |

## Enter and exit

Combine 8–20 px of travel with opacity. Large travel distances make diagrams feel like slide decks rather than systems.

## Sequential reveal

Stagger related items by 120–300 ms. Preserve enough overlap that the viewer perceives them as one group.

## Flow along a connector

Choose one:

- a token moving along the connector;
- a short highlighted dash with animated `stroke-dashoffset`;
- connector color/width emphasis;
- progressive path drawing.

Do not use all four simultaneously unless the flow is the sole subject.

## Processing state

Use a slow pulse, rotating short arc, or 3–5 sequential dots. Avoid high-frequency flashing.

## State transition

Crossfade old/new labels while the container remains stable. Stable geometry reduces cognitive load.

## Bar and chart growth

Animate from a meaningful baseline. For horizontal bars, scale a wrapper from the left edge or animate width. Set `transform-origin` explicitly in web mode. In pure SVG, nested groups with `animateTransform type="scale"` are reliable.

## Emphasis pop

Use a restrained key sequence such as `1 → 1.08 → .98 → 1` over 300–500 ms. Apply it once per important event, not continuously.

## Camera-like transitions

Avoid animating `viewBox` unless a true pan/zoom narrative is necessary. Moving the scene inside a clipped viewport is often easier to control and debug.

## Loop reset

Reset during a fade or after a stationary pause. If the beginning and ending compositions differ greatly, consider alternating or a non-looping sequence with replay controls.
