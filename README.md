# qtng/cdn

The font files of [qatt.org](https://qatt.org/) and [chunom.org](https://chunom.org/), in one place for other sites and for the downloads.

- `fonts/`: the QATT fonts (`qatt-*.ttf`, `.woff2`, the QATT letters `*-letters.*`) and the big fonts with Chữ Nôm for the desktop (`qatt-pen[-thin|-light|-medium].ttf`, `migoi.ttf`, `celluloid.ttf`, `phongthao.ttf`).
- `fonts/web/`: the web files of the big fonts: the CJK part in slices (`<font>-NN.woff2`, each with its `unicode-range`) and the Latin (`<font>-latin.woff2`).
- Licence: `fonts/LICENSE.txt`.

Served at

- `https://cdn.jsdelivr.net/gh/qtng/cdn@main/fonts/…` (jsDelivr; files up to 20 MB: the web files, not the big `.ttf`),
- `https://chunom.org/cdn/fonts/…` (GitHub Pages of this repository).

To use the fonts on a web page, load the script `https://qatt.org/cdn/v1/webfonts.js?family=QATT+Pen` (see its head for the parameters); the font catalogue is https://chunom.org/chunom/fonts/.

The files are built elsewhere and copied here; do not edit them by hand.
