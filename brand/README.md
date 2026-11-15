Winterloom builds agentic software for esoteric niches with an asymmetric edge. The brand looks and talks like a cold terminal: one monospace face, pale phosphor on dark glass, a shell prompt and a blinking block cursor. Keep every surface as quiet as a login screen.

## Voice and copy

- Write everything in lowercase, including the name: `winterloom`. Sentence punctuation stays (a mission line ends with a full stop).
- Present content as a terminal session. A command in `dim` after the prompt `~ $ `, then its output in `phosphor`:
  - `~ $ whoami` → `winterloom`
  - `~ $ cat mission` → `agentic software for esoteric niches with an asymmetric edge.`
  - `~ $ contact` → `elijah@winterloom.ai`
- Commands are short real-looking shell words (`whoami`, `cat`, `ls`, `man`, `status`). Avoid jokes that break the fiction, such as fake error codes or hacker slang.
- Boot and status lines use `·` as a separator and read like system output: `wl-os 0.1 · tty1 · 06 nov 2026 · cold boot ok`.
- No emoji, no exclamation marks, no marketing superlatives. Say what the thing does in one plain line.

## Colour

- Two themes. `tube` (dark) is the primary and the default for screens. `paper` (light) is for print, documents and anywhere a dark page would be wrong.
- Set pages on `glass`. Use `glass-raised` only for a single raised element: an app tile, a code block, the glow at the centre of a screen.
- Text is `phosphor`. Prompts, boot lines and captions are `dim`. Never introduce a third text grey.
- `frost` is the only accent. Use it for links, the focus ring and at most one highlighted word per screen. It never fills a large area.
- `rule` is for hairlines and scanline tint only.
- Focus ring: a solid 1px `frost` outline, 3px offset. It holds at least 5:1 on `glass` in both themes.

## Type

- One family: VT323 (`fonts/VT323-Regular.woff2`, family key `mono`). Never pair it with a second display face. IBM Plex Mono is only a fallback.
- Styles: `display` 112px for the name on a landing screen (56px on phones), `title` 48px for section heads and product names, `body` 24px for running text, `small` 19px for boot lines and captions. VT323 runs small, so nothing is set below 19px.
- Keep lines near 58 characters and set them flush left in one column. Centre only the column itself on the page.

## Space, shape and effects

- Spacing comes from `space-1` to `space-5`. Command blocks in a session are `space-4` apart, a command sits `space-2` above its output, and a screen has `space-5` top and bottom.
- Every corner is `radius-none`. No rounded boxes, pills or cards.
- On screen, phosphor text gets a faint glow (a 2px halo of `phosphor` plus a 10px halo of `frost` at about 18%), and the cursor uses `glow-cursor`. Scanlines run every 3px in black at about 28% opacity. Paper has no glow and no scanlines.
- Motion is limited to the cursor blinking (about 1.06s, stepped) and a rare faint flicker of the scanlines. Both stop under reduced motion. No typing animations, rain, neon or gradients.

## Logo system

All logos are built from two things on VT323's own pixel grid: **VT323 glyph outlines** and **the block cursor**. One dot is 40 font units (1/25 em). Each glyph advances 10 dots.

- **The cursor** is 8 × 16 dots, runs from 2 dots below the baseline to cap height, and sits 1 dot after the last glyph. It is always last and always solid `phosphor`.
- **Wordmark** (`wordmark-*`): `winterloom` followed by the cursor. The primary logo.
- **Plain wordmark** (`wordmark-plain-*`): no cursor. Use it inside running text, footers, and anywhere a cursor would look like a typo.
- **Prompt lockup** (`prompt-*`): `~ $ ` in `dim`, then the wordmark. Use it for headers and title cards that open a session.
- **Mark** (`mark-*`): `w` plus the cursor. Use it where the wordmark will not fit.
- **App icon** (`icon-*`): the mark centred on a square `glass` tile with about 17% margin. Square corners; the platform rounds them if it must.
- **Product lockups**: `winterloom/<product>` with the slash and product name in `dim`, then the cursor, as in `winterloom-oracle-*`. Product names are one lowercase word.
- Every logo uses a single ink plus `dim`, comes in `on-dark` (phosphor `#cfe8f2`, dim `#6b8794`) and `on-light` (ink `#0d1a20`, dim `#4d626c`) versions, and stays outlined so it renders without the font.
- Clear space is 2 character cells (20 dots) on every side. Minimum widths: wordmark 96px, mark and icon 16px.
- Do not: set the name in capitals, change the font, add a gradient or neon glow to the files, stretch the cursor, move the cursor anywhere but the end, or put a logo on a ground other than `glass`, `glass-raised` or plain black or white.

### Generating new logos

`source/gen_logos.py` outlines any text with these rules. With the font file and an output folder it writes the standard set; extra arguments make product lockups:

```
pip install fonttools brotli
python3 source/gen_logos.py fonts/VT323-Regular.woff2 out
python3 source/gen_logos.py fonts/VT323-Regular.woff2 out "winterloom/oracle" "winterloom/ledger"
```

## Iconography and imagery

- No icon set. Use VT323 characters as icons: `>` for go, `~` for home, `/` for paths, `·` as a separator, `█` for the cursor.
- No photography or illustration. When an image is unavoidable, show a screen: text on `glass` with scanlines, or one of the blackwork patterns below.

## Pattern: op-art blackwork

The brand's one image language, for notes, covers, dividers and the backs of things. It borrows from geometric blackwork tattooing (heavy solid ink, echoed contour lines, grids pulled into depth, a sacred-geometry focal point, dotwork shading) and puts it through a one-bit terminal: every pattern is a bitmap on the dot grid where each dot is either ink or ground.

### The rules

- **One bit.** Ink is `phosphor` on `glass` in either theme: `#cfe8f2` on `#05080b` (on-dark) or `#0d1a20` on `#eef2f3` (on-light). No greys, no gradients, no anti-aliasing, no `frost`. Render with `shape-rendering: crispEdges` or `image-rendering: pixelated`.
- **Tone comes from spacing.** Shade by changing the gap between lines or with ordered (Bayer) dither. Never use opacity or a tint to make something lighter.
- **Echo the contour.** A shape is drawn by its contour repeated outward at an even pitch (2 to 3 dots ink, the same in ground). Where two echo fields meet, let them fold into chevrons.
- **Warp the grid.** Grids may bulge, pinch or fan, but lines stay continuous and the cell count stays readable.
- **One quiet thing.** Every busy pattern holds at most one still point: the eye, a lattice diamond or a single orb, set on a plate of clear ground at least 3 dots wide. Never two.
- **The eye** is a vesica almond (two circles) with a solid pupil and a single 1-dot highlight notch. It is the brand's watching eye and the only figurative motif. No faces, bodies, hands or creatures.
- **Square and on grid.** Patterns are square tiles of 128 dots or bands 16 dots tall. Scale only by whole multiples (8× gives 1024px), so dots stay square.
- **Patterns never touch type.** Keep a clear-space margin of 2 character cells between any pattern and text or a logo, and never set text over a pattern. A logo may sit on the eye plate of `field` only.
- **Screen effects stay off.** Glow and scanlines belong to text. Patterns are flat.

### Where it goes

- Notes and docs: one `rule` band as a section divider, or one tile as a cover image. One pattern per page.
- Screens: a tile as the background of an empty state or a loading screen, behind nothing.
- Never in the logo, the app icon, the favicon or body text areas.

### The set (`patterns/`)

Each comes as `<name>-on-dark.svg` and `<name>-on-light.svg`, with 1024px PNGs (8× nearest-neighbour) in `patterns/png/`. Contact sheets: `patterns/png/sheet-on-dark.png` and `sheet-on-light.png`.

| name | what it is | use |
| --- | --- | --- |
| `contour` | echoed contour bands around three seeds, folding into chevrons where they meet | busy ground, covers |
| `warp` | a square grid pulled into a lens | covers, technical notes |
| `rays` | rays fanning from a lattice diamond | title cards, the start of a long doc |
| `eye` | the watching eye, echoed outward in vesica bands | the quiet ornament on its own; small sizes |
| `dotwork` | a dithered orb and ring, shaded only by stipple | empty states, research notes |
| `field` | the composition rule in one tile: busy echoes around one eye on a clear plate | hero image, back covers |
| `rule` | an echoed zigzag band, 256 × 16 dots | section dividers in notes |

### Generating new patterns

`source/gen_patterns.py` builds each pattern from distance fields (bands of distance for echoes, a smooth minimum for chevrons, a radial warp for lenses, Bayer dither for dotwork) and writes both themes as SVG and PNG. Add a function to `PATTERNS` to make a new one.

```
pip install numpy pillow
python3 source/gen_patterns.py patterns 8
```

