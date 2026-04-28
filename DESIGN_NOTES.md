# Design Notes — Phuket Interactive Textbook

A visual and component reference. When building a new chapter, match these patterns unless there's a reason not to.

## Color palette

```css
--paper:      #ede4d3;   /* main background — warm aged paper */
--paper-dark: #d8cdb6;   /* secondary surfaces */
--ink:        #2b1d12;   /* primary text — very dark brown, not pure black */
--ink-soft:   #5a4530;   /* secondary text, captions, metadata */
--accent:     #a8331f;   /* the only "loud" color — used sparingly for emphasis */
```

For data visualization in chapters that need more colors, use this earth-tone family (already used in the migrations map):

```
#1f5b6b  teal blue       (sea / water themes)
#8a6d2c  ochre           (earth / trade)
#3f6b3a  forest green    (vegetation / Islam)
#a8331f  brick red       (Siamese / accent)
#6b3070  aubergine       (European)
#b8761f  amber           (Chinese)
#5a4530  deep umber      (overland / Burmese)
#2b1d12  ink brown       (modern / global)
```

## Typography

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

- **Cormorant Garamond** — body text, headings, titles. Weights 400 / 500 / 600 / 700, plus italic 400.
- **JetBrains Mono** — small uppercase labels, metadata, coordinates, technical chrome. Weights 400 / 500.

Type rules of thumb:

- Headings: weight 600, slight negative letter-spacing on h1 (`letter-spacing: -.01em`).
- Italics in headings (using `<em>`) are styled in `var(--accent)` for one-word emphasis. See "A Thousand Years of *Arrivals*".
- Small caps labels ("WAVES OF MIGRATION") use JetBrains Mono at ~0.65rem with `letter-spacing: 0.25em–0.3em` and `text-transform: uppercase`.
- Body prose is roughly 1rem with `line-height: 1.5`. Don't go smaller than 0.85rem for sustained reading.

## Recurring components

### Eyebrow label
A small mono caps label above a heading, used to tag the chapter or section.
```html
<div class="eyebrow">Vol. I — Indian Ocean Studies</div>
```

### Title with accented italic
```html
<h1>A Thousand Years of <em>Arrivals</em></h1>
```

### Subtitle / dek
Italic, ink-soft color, with a hairline border below.
```html
<p class="subtitle">Migrations, traders, and settlers who shaped...</p>
```

### Section divider (hairline with caps label)
```html
<div class="legend-title">Waves of Migration</div>
```
The CSS uses a `::after` pseudo-element to draw a hairline that fills the rest of the row. See migrations-map.html.

### Detail card / cartouche
Used for the slide-out info panel in the map chapter. Paper-on-paper with a subtle border and offset shadow that mimics a paper-pasted-on-paper look. The double-border effect uses an inset `::before`.

### Metadata strip
Two pieces of metadata side-by-side, separated from the prose above and below by hairline rules. Mono font, very small.
```html
<div class="detail-meta">
  <span><strong>Period:</strong> c. 1000 – 1400 CE</span>
  <span><strong>Origin:</strong> Coromandel Coast</span>
</div>
```

### Map cartouche (corner label)
A floating block in the corner of a map giving location context, with `backdrop-filter: blur(2px)` for readability over imagery.

### Pulsing destination dot
A CSS `@keyframes pulse` animation expanding a ring outward from a static dot. Used to mark the focal point (Phuket itself).

## Map styling (Leaflet)

When using Leaflet, apply these filters to make tiles match the paper aesthetic:

```css
.leaflet-tile {
  filter: sepia(.4) saturate(.7) brightness(1.05) contrast(.95);
  mix-blend-mode: multiply;
}
.leaflet-container {
  background: #c9bfa6;
  font-family: 'Cormorant Garamond', serif;
}
```

Use the **CARTO light_nolabels** tile layer — clean, label-free, lets you place your own typography:
```
https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png
```

For routes/lines: 2.5px weight by default, 0.85 opacity, rounded line caps. Add a darker shadow line behind (5px, 0.12 opacity) for depth.

## Responsive layout pattern

Two-column desktop layout (sidebar + main content) becomes a stacked layout on mobile. Always main content first, sidebar second on mobile.

```css
.layout { display: grid; grid-template-columns: 380px 1fr; height: 100vh; }

@media (max-width: 900px) {
  html, body { height: auto; }
  .layout { grid-template-columns: 1fr; height: auto; min-height: 100vh; }
  .sidebar { order: 2; }
  .main-content { order: 1; height: 65vh; min-height: 400px; }
}
```

## Loading state pattern

Every chapter that loads external resources (maps, images, fonts) should have a loading state with a hard timeout. Pattern:

```js
const safetyTimeout = setTimeout(() => statusEl.classList.add('hidden'), 8000);
tileLayer.on('load', () => {
  clearTimeout(safetyTimeout);
  statusEl.classList.add('hidden');
});
```

A loading screen that hangs forever is the worst failure mode. Always have an escape hatch.

## What to avoid

- Heavy drop shadows, glassmorphism, neon gradients, glowing borders.
- Emoji in UI chrome.
- Decorative dividers, ornate borders, "vintage" textures applied as image backgrounds.
- More than one accent color per page.
- Centered body text for long-form prose.
- Hover-only interactions (the user is on mobile half the time).
- Animations that loop forever in the user's peripheral vision (the pulsing dot is the one exception, and it's small).
