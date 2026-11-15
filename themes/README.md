# Style variants

Slidev only loads the root `style.css`. To switch the look, copy a variant over it before `npm run dev` / `npm run build`:

```bash
cp themes/style-nordic.css style.css     # and back: cp themes/style-warm.css style.css
```

| file | look | fonts |
|---|---|---|
| `style-warm.css` | original IE-day deck: cream, orange, near-black | Raleway |
| `style-nordic.css` | cool slate background, teal accent, dark slate covers | Inter |
| `style-forest.css` | sage paper, green accent, deep green covers | Source Sans 3 |
| `style-list.css` | LIST brand: plum covers, LIST magenta accent, cyan on dark | IBM Plex Sans |
| `style-academic.css` | warm white paper, navy accent and covers | Source Serif 4 (headings), Source Sans 3 (text) |
| `style-indigo.css` | lavender paper, violet accent, near-black indigo covers | Space Grotesk (headings), Inter (text) |

All variants share the same layout rules and variable names (`--ie-orange` is the accent, `--ie-cream` the light
background and the text colour on dark slides), so slides and components need no changes. Each non-warm variant ends
with a "Theme overrides" block that:

- sets `--font-head` for titles and number blocks, and a lighter `--ie-accent-on-dark` for cover, section and closing slides;
- remaps the deck colours hard-coded in `figures/*.svg` (`#f46524`, `#f8bd90`, `#353535`, `#fcf6d7`, ...) to the theme
  variables (figures taken from papers keep their own colours);
- replaces the warm hover and tag tints hard-coded in the provenance and JSON explorer components.

Fonts (SIL Open Font License) are shipped in `public/fonts/<family>/` with their `OFL.txt`.
