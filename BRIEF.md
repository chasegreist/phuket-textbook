# Phuket: An Interactive History — Project Brief

## What this is

An **interactive HTML textbook** about the history, peoples, and cultures of Phuket, Thailand. Built as static HTML/CSS/JS that runs in any browser without a server. The audience is curious adults — visitors, students, residents — who want a richer understanding of the island than a guidebook offers.

The current state of the project is a **single working artifact**: `migrations-map.html` — an interactive map showing eight waves of migration into Phuket over the last thousand years, with historically accurate sea routes (Portuguese around the Cape of Good Hope, Hokkien Chinese hugging the South China Sea coast, Tamils across the Bay of Bengal via Takua Pa, etc.). This is **chapter one** of a planned multi-chapter interactive textbook.

## Design philosophy

The aesthetic established in the migrations map should carry through the whole project:

- **Editorial atlas / explorer's journal** feel — warm paper background (`#ede4d3`), dark ink (`#2b1d12`), a single restrained accent red (`#a8331f`).
- **Cormorant Garamond** for prose and titles (italics used freely), **JetBrains Mono** for small caps / metadata / labels.
- **Generous whitespace, restrained UI chrome.** No drop shadows on every card. No rainbow gradients. No emoji.
- **Show the data, not the framing.** If a chapter is about migration, the map dominates the screen; the chrome around it is quiet.
- **Real, accurate content over decoration.** Every claim should be defensible. Routes follow real geography. Dates, place names, and ethnonyms should be correct.

When in doubt, look at how `migrations-map.html` handles things — sidebar list, detail card with metadata strip, route breadcrumb, sepia-filtered map tiles, pulsing destination dot — and stay in that visual vocabulary.

## Technical constraints

- **Static HTML/CSS/JS only.** No build step, no React, no npm. Each chapter is one self-contained `.html` file that can be opened with a double-click.
- **CDN libraries are fine** (Leaflet for maps, fonts from Google Fonts). Keep dependencies minimal — vanilla JS where possible.
- **Mobile-first responsive.** The user reads on Android in the Claude app and on desktop. At narrow widths, sidebars become stacked sections; maps shrink to ~65vh.
- **Robust loading.** Always include a safety timeout for any asset that might not load (see how the map artifact handles this with the 8-second timeout).
- **No localStorage, no sessionStorage** — these don't work in some embedded browsers. Keep all state in memory.

## Proposed chapter structure

The user will refine this, but a strong starting outline:

1. **A Thousand Years of Arrivals** — migrations map *(already built)*
2. **The Tin Island** — economic history: Phuket's tin trade, the rise of Phuket Town, the Sino-Portuguese architecture, the shift to rubber and then tourism. Could be a scrollytelling piece with archival photos and an animated timeline.
3. **Faiths of the Island** — religious geography. Interactive map of major Buddhist temples, Chinese shrines, mosques, Hindu temples, the Vegetarian Festival, Thai Pak Klang. Filter by religion and era.
4. **The Vegetarian Festival** — a deep dive into the nine-day Taoist festival, its Hokkien origins, its rituals, its meaning. Could be a long-form illustrated essay with a calendar visualization.
5. **Phuket Town: A Walking Tour** — an interactive map of the old town's Sino-Portuguese shophouses, tied to short essays about each landmark (Thavorn Hotel, Standard Chartered building, Thai Hua Museum, the Old Post Office, etc.).
6. **The 2004 Tsunami** — a careful, respectful chapter. Map of impact zones, timeline of the morning, memorial sites, recovery story.
7. **Beaches & Geography** — the physical island. Interactive map of beaches with characteristics (west coast vs east coast, monsoon seasons, mangroves, limestone karsts of Phang Nga Bay).
8. **Languages You'll Hear** — Thai, Southern Thai dialect, Hokkien, Burmese, Russian, English. Audio samples if practical, with notes on where each is spoken on the island.

Each chapter should be a separate HTML file, but they share a common visual language and a top-level **index page** that frames the textbook and links them all together.

## What I'd like Claude Code to do

### First task: build the index / table of contents

Create `index.html` — the textbook's cover and table of contents. It should:

- Open with a strong visual: maybe a sepia-toned map of Phuket itself, or an evocative title page in the same paper-and-ink aesthetic.
- List all planned chapters with short descriptions, even ones not yet built (mark unbuilt chapters as "Coming soon").
- Link to the existing `migrations-map.html` as Chapter 1.
- Establish the shared design tokens (CSS variables) in a way that future chapters can reuse.

### Second task: extract the shared styles

The migrations map currently has all its CSS inline. Pull out the shared design tokens (colors, fonts, the paper background, the cartouche, the eyebrow text style, etc.) into a single `styles/textbook.css` that every chapter can link to. Each chapter keeps its own page-specific styles inline or in its own file.

### Third task: pick the next chapter and build it

Ask the user which chapter they want next. My guess is **Chapter 2: The Tin Island** would be a natural follow-up since it builds on the migration story (especially the Hokkien wave). But let the user choose.

### Ongoing: keep the content honest

Phuket has real history — some of it painful (the tsunami, labor exploitation in the tin mines, ongoing issues with stateless Chao Le and undocumented Burmese workers). Don't sanitize it. Don't sensationalize it either. The tone is the calm, accurate voice of a good museum exhibit.

When facts matter — dates, names, statistics, ethnographic details — **verify with web search** before writing. The current migrations map was fact-checked this way and it shows.

## Files included in this handoff

- `migrations-map.html` — the working chapter 1, fully interactive
- `BRIEF.md` — this file
- `DESIGN_NOTES.md` — visual reference: colors, fonts, components, patterns
- `CHAPTER_IDEAS.md` — expanded notes on each proposed chapter

## Notes on working with this project

- The user is a coding beginner. Explain your changes plainly. Don't refactor heavily without asking.
- The user is in Thailand and may know far more about Phuket than your training data does. If they correct a fact, trust them and update.
- Keep each chapter under ~1000 lines if possible. Split into separate files if it gets bigger.
- Test on mobile mentally — narrow screens, slow connections, sometimes flaky tile servers.
