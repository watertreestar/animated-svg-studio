# WeChat and constrained rich-text mode

This profile targets environments that sanitize article HTML and allow only a subset of SVG. Exact behavior can change between editor, preview, mobile app, and desktop client, so validate and test a real draft before publication.

## Conservative baseline

Prefer:

- inline `<svg>` with explicit `viewBox`, width, and height;
- basic shapes, paths, groups, text, and raster `<image>`;
- presentation attributes such as `fill`, `stroke`, and `opacity`;
- SMIL `<animate>` and `<animateTransform>`;
- `repeatCount="indefinite"` for passive loops;
- a meaningful static first frame.

Avoid:

- JavaScript and `<script>`;
- inline `onclick` and other event handlers unless a tested interaction recipe requires one;
- CSS `@keyframes`, transitions, external stylesheets, and complex selectors;
- `foreignObject`;
- remote fonts;
- fragile external URL references;
- filters and masks when a simpler shape can produce the same result;
- critical reliance on `<use>` clones;
- unsupported HTML controls inside the SVG.

## Images

Use a publisher-approved image host. For rounded image corners, a pattern-filled rounded `<rect>` can be more reliable than clipping in some clients:

```xml
<defs>
  <pattern id="photo" width="1" height="1" patternContentUnits="objectBoundingBox">
    <image href="https://approved-host/image.jpg" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
  </pattern>
</defs>
<rect x="20" y="20" width="180" height="120" rx="16" fill="url(#photo)"/>
```

Test this exact pattern in the destination editor because sanitizer behavior is not standardized.

When reproducing or archiving authorized material for study, do not leave third-party image-host URLs in the deliverable. Download permitted assets, preserve attribution metadata, and rewrite SVG `href` values to local relative assets. When publishing new content, upload those local images through the destination account's own editor or an approved image host; a local filesystem path itself will not work after publication.

## Click interactions

Click-triggered SMIL support is less reliable than passive looping. If the user requests interaction:

1. Build a useful passive/static fallback first.
2. Keep the click target large and visible.
3. Avoid cross-element event references unless tested.
4. Test in the actual mobile client, not only Chrome.
5. Explain that publication behavior may change after editor sanitization.

## Publishing workflow

1. Generate a self-contained HTML preview containing the SVG.
2. Validate with `--profile wechat`.
3. Open in Chrome or Safari and copy the rendered SVG if the editor workflow requires paste-in content.
4. Paste into a draft article.
5. Preview on iOS, Android, and desktop when the audience warrants it.
6. Keep a static image fallback ready.

Do not promise universal compatibility; report the tested clients and date.
