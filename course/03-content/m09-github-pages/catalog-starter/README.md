# Catalog starter

A product catalog you can publish with GitHub Pages. Plain HTML, CSS and JavaScript: no build step,
no framework, nothing to install. Double-click `index.html` and it opens in your browser exactly as
it will look online.

| File | What it is | Do you edit it? |
|---|---|---|
| `products.js` | your store name, your contact link, and your products | **Yes — this is the one you change** |
| `index.html` | the page itself | Only the two lines marked near the top |
| `styles.css` | colours and layout | If you want different colours: change `:root` |
| `app.js` | draws the products, the filters, search and sort | No |
| `.nojekyll` | an empty file that tells GitHub Pages to publish these files as they are | No — keep it |

## Change the products

Open `products.js` in your editor. Each product is a block between `{` and `}`:

```js
{
  id: "everyday-mug",            // short, lowercase, no spaces; also the link #everyday-mug
  name: "Everyday Mug",
  category: "Mugs",              // one filter button appears per category
  price: 32,                     // a number, no currency sign
  summary: "A 350 ml mug with a thumb rest.",
  tags: ["dishwasher safe"],     // optional
  image: "images/mug.jpg",       // optional; without it the card shows a coloured tile
  color: "#b9a88f",              // optional; the tile colour when there is no image
  buyUrl: ""                     // optional; a checkout link hosted somewhere else
}
```

Blocks are separated by commas. A missing comma is the most common mistake; if the page shows
"products.js did not load", that is almost always why.

To add photos, make a folder called `images` next to `index.html`, put the files in it, and set
`image: "images/your-file.jpg"`. Keep each photo under about 500 KB so the page loads fast.

## What GitHub Pages is for, and what it is not

GitHub Pages hosts a site that **shows** your products. Its terms do not allow using it to run an
online shop or any site whose main purpose is taking payments. So this catalog has no cart and no
checkout. Each product can link out with `buyUrl` to a checkout you run elsewhere — a payment link
from a payment provider, or a listing on a marketplace — and without one the button becomes
"Ask about this", which opens an email to the address in `store.contact`.

## Publish it

The full walkthrough, for Windows and macOS, is Lab M9 in
`course/03-content/m09-github-pages/lab.md`. The short version: put these files in the top folder
of a public repository, push, then in the repository open **Settings → Pages**, set **Source** to
**Deploy from a branch**, choose `main` and `/ (root)`, and **Save**. The site appears at
`https://<your-username>.github.io/<repository-name>/` — it can take up to 10 minutes.

## Verified

Checked in a headless Chromium, opened from disk with `file://`, at 390 px and 1280 px wide, in
light and dark mode: 6 products render, the category filter, search and sort work, nothing scrolls
sideways, no console errors, and every text element meets WCAG AA contrast.
