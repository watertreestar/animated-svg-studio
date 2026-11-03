---
name: animated-svg-studio
description: Design, generate, debug, validate, and package animated SVGs and SVG-based explainers for websites, standalone files, React, Vue, documentation, presentations, email-safe fallbacks, and constrained publishing platforms such as WeChat. Use this skill whenever the user asks for an SVG animation, animated diagram, architecture animation, interactive infographic, motion icon, data-flow visualization, SVG component, SMIL animation, SVG compatibility repair, or wants to turn prose or a static diagram into an animated visual—even if they do not explicitly say “SVG skill.”
compatibility: Requires Python 3.9+ for bundled validation and preview scripts. Browser automation is optional but recommended for visual verification.
---

# Animated SVG Studio

Create purposeful, portable SVG motion rather than decorative motion for its own sake. Treat the SVG as a small visual system: establish a scene, define the message, design a synchronized timeline, implement it with the least complex compatible technology, then validate and preview it.

## Start here

1. Determine the target environment and intended interaction.
2. Translate the content into a visual storyboard.
3. Choose the animation runtime using the table below.
4. Generate source files in a dedicated output directory.
5. Run the bundled validator with the matching profile.
6. Build an independent preview page.
7. Visually inspect at desktop and mobile widths when browser tools are available.
8. Report files created, runtime choice, validation status, and any compatibility caveats.

If the user did not specify a target, default to **portable SMIL SVG plus a standalone HTML preview**. This gives a script-free source artifact while preserving an easy review experience.

## Choose an output mode

| User target | Preferred implementation | Profile |
|---|---|---|
| Standalone `.svg`, Markdown, docs | SVG + SMIL | `pure-svg` |
| General website or interactive demo | Inline SVG + CSS/JS or Web Animations API | `web` |
| React application | TSX component; CSS/WAAPI unless SMIL is preferable | `web` |
| Vue application | Vue SFC; CSS/WAAPI unless SMIL is preferable | `web` |
| WeChat/strict rich-text publisher | Inline SVG + conservative SMIL only | `wechat` |
| Email or unknown sanitizer | Static SVG/PNG fallback; animation is progressive enhancement | `email` |
| Slide or video export | SVG master plus raster/video export instructions | `pure-svg` |

Read the relevant reference before implementation:

- SMIL and standalone SVG: `references/smil-guide.md`
- CSS, JavaScript, and web interaction: `references/web-mode.md`
- React and Vue components: `references/framework-mode.md`
- constrained rich-text and WeChat: `references/wechat-mode.md`
- visual patterns and timing recipes: `references/animation-patterns.md`
- accessibility and motion safety: `references/accessibility.md`
- support and fallbacks: `references/compatibility.md`
- ready-to-adapt examples: `examples/README.md`
- article-inspired warm editorial theme: `references/editorial-theme.md`
- selectable theme system: `references/themes.md` and `assets/themes.json`
- Chinese examples organized by theme: `examples/zh/README.md`

When the request resembles an included example, inspect that source before generating a new artifact. Reuse its structural pattern, not its labels, colors, or exact composition. This reduces avoidable timeline and compatibility mistakes without making every result look the same.

For article explainers and technical diagrams, default to the warm editorial theme unless the user supplies brand guidance. Use its Chinese-first font stack, warm paper background, dark brown-black text, muted taupe labels, vermilion emphasis, and restrained green/gold secondary accents.

The theme ID `default-editorial` is the general default. When the user requests another look, select a bundled theme or create a custom token set. Read `references/themes.md` before recoloring. A theme change must update the complete semantic palette—background, typography, cards, connectors, active state, and secondary series—not only the canvas background.

Choose a theme directory under `examples/zh/`, then inspect the example matching the required layout. Theme variants deliberately keep equivalent geometry so the visual skin can be changed without unexpectedly redesigning the composition.

## Clarify only consequential ambiguity

Do not block on minor choices. Infer a restrained visual style and state assumptions. Ask only when an answer changes the architecture, such as:

- Where will it run?
- Must it be a single SVG file?
- Is interaction required, or only looping playback?
- Are there brand colors, exact dimensions, or supplied assets?
- Does the user need editable source, a framework component, or an exported media file?

## Storyboard before coding

For diagrams and explainers, write a compact internal storyboard:

1. **Message:** one sentence describing what the viewer should understand.
2. **Actors:** 3–7 primary objects; group secondary details.
3. **Sequence:** 3–6 beats, each with a clear visual change.
4. **Emphasis:** identify the one active object per beat where possible.
5. **Loop/reset:** return without a distracting jump, or end intentionally.

Prefer one coherent sequence over many unrelated looping effects. A useful default loop is 5–8 seconds with a 0.6–1.2 second reading pause at the end.

## Build the SVG as a system

Use this layer order unless the design requires otherwise:

1. Background and frame
2. Connectors and paths
3. Primary nodes/cards
4. Status indicators and moving tokens
5. Labels and annotations
6. Interaction hit areas, when supported

Use semantic group IDs such as `router-card`, `worker-nodes`, and `flow-token`, not generated IDs such as `layer17-copy-3`. Keep transforms on wrapper `<g>` elements so layout transforms do not fight animation transforms.

Always include:

- `xmlns="http://www.w3.org/2000/svg"`
- a `viewBox`
- responsive sizing unless fixed dimensions are required
- `<title>` and, for explanatory visuals, `<desc>`
- a predictable font stack or converted vector assets when exact typography is essential

## Animation design rules

- Animate `transform` and `opacity` first; they are efficient and visually stable.
- Use `stroke-dashoffset` for path drawing and flow, not hundreds of tiny elements.
- Synchronize related elements to one master duration.
- Use normalized `keyTimes` for SMIL timelines.
- Reserve elastic overshoot for small emphasis moments; avoid making the whole diagram bounce.
- Give text enough stationary time to be read.
- Avoid rapid flashing. Never create more than three flashes per second.
- Make the first frame meaningful because some platforms or exports may freeze there.
- Make the final frame meaningful for non-looping animations.

## Implementation workflow

### 1. Create source artifacts

Normally create:

```text
output/
├── animation.svg
├── preview.html
└── validation.json
```

For frameworks, replace or supplement `animation.svg` with `AnimatedDiagram.tsx` or `AnimatedDiagram.vue`. Keep a plain SVG reference version when practical because it simplifies inspection and reuse.

### 2. Validate

Run from the skill directory:

```bash
python scripts/validate_svg.py output/animation.svg --profile pure-svg --json output/validation.json
```

Profiles:

- `web`: permits scripting and web interaction but still reports risky constructs.
- `pure-svg`: rejects scripts and inline event handlers; allows SMIL.
- `wechat`: applies conservative rich-text SVG restrictions.
- `email`: expects a static, self-contained fallback.

Treat validator errors as blockers. Review warnings rather than blindly suppressing them. If a warning is intentional, explain it in the final response.

### 3. Build a preview

```bash
python scripts/build_preview.py output/animation.svg -o output/preview.html --title "Animated SVG preview"
```

The generated preview supports responsive viewing, a motion toggle, replay, SVG download, and source copy. The copy action is a preview convenience; the SVG itself remains independently usable.

### 4. Inspect compatibility

```bash
python scripts/inspect_compatibility.py output/animation.svg
```

Use this when the target is uncertain or the user wants to publish to several environments. It produces a profile matrix rather than choosing for the user.

### 5. Optimize conservatively

```bash
python scripts/optimize_svg.py output/animation.svg -o output/animation.min.svg
```

The bundled optimizer removes comments, editor metadata, and redundant whitespace. It deliberately avoids aggressive path rewriting that could break animation targets. Preserve the editable source alongside the optimized output.

### 6. Visually verify

When browser tooling is available:

- open `preview.html`;
- inspect one complete loop;
- resize to approximately 390 px and 1280 px widths;
- verify text does not clip or overflow;
- verify the replay and motion controls;
- check the browser console;
- capture a screenshot when useful to the user.

Do not claim visual verification if only source validation was performed.

## Platform-specific rules

### Pure SVG / SMIL

Keep all animation declarative. Do not use JavaScript, inline handlers, or HTML inside `foreignObject`. Use `<animate>`, `<animateTransform>`, and `<animateMotion>` only where they improve clarity. See `references/smil-guide.md`.

### Web

Use CSS for simple state transitions and loops. Use Web Animations API or a small script when interaction, replay, scroll control, or dynamic data requires it. Do not add a framework solely for animation. See `references/web-mode.md`.

### React and Vue

Use framework-safe attribute names and scoped component state. Avoid IDs that collide when multiple component instances render. Prefix IDs with `useId()` in React or a per-instance value in Vue. See `references/framework-mode.md`.

### WeChat and constrained publishers

Assume sanitization. Avoid JavaScript, CSS keyframes, `foreignObject`, external stylesheets, and fragile event references. Prefer SMIL attributes directly on SVG elements. Provide a static fallback when publication reliability matters. See `references/wechat-mode.md`.

### Email

Treat animation as optional. Produce a useful static first frame and recommend PNG/GIF only when the receiving clients have been tested. Never make essential information animation-only.

## Editing an existing SVG

1. Preserve the original file unless the user explicitly requests in-place edits.
2. Inspect IDs, dependencies, styles, and animation targets.
3. Run validation before changing it to establish a baseline.
4. Make the smallest coherent change.
5. Validate again and compare warnings.
6. Preview the entire loop, not only the edited instant.

## Quality checklist

Before delivery, confirm:

- The animation communicates the requested idea.
- The target profile matches the destination.
- The SVG has a `viewBox`, title, and description.
- IDs are unique and references resolve.
- Timeline durations and repeats are intentional.
- Text remains readable at narrow widths.
- The first frame works as a fallback.
- Reduced-motion behavior or a static fallback exists where relevant.
- No unrequested tracking, network calls, or hidden scripts were added.
- Validation completed without errors.

## Final response format

Lead with the result. Include:

1. Files created with paths
2. Chosen runtime/profile and why
3. Validation and visual verification status
4. Important embedding or publishing instructions
5. Any known limitations

Do not paste the entire SVG into chat when a file has been created unless the user asks for the source inline.
