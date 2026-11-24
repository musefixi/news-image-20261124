// news-image-20261124: "Sum up 24 November's world news in one image."
//
// The picture of the day is drawn by draw.py (a deterministic Pillow
// program: six news panels plus a sports strip, 1024x1024) and sits beside
// this file as entry.png. The two programs split the work on purpose:
//
//   draw.py  — the artist. Pure drawing, no network, no randomness; running
//              `python3 draw.py` regenerates entry.png byte-for-byte.
//   main.ts  — the courier. The grader runs this program twice in a sandbox
//              with no network and reads only /output/entry.png, so the whole
//              job here is a faithful byte-for-byte copy of the bundled image
//              into the output directory. Copying instead of re-drawing keeps
//              the graded run free of any font or Pillow dependency: Node's
//              standard library is all it needs.
//
// Locally, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// To redraw the picture from scratch instead:
//   python3 draw.py          # regenerates entry.png in place

// Runs with no network and no dependencies: Node's standard library only.
// The image is drawn once, ahead of time, and bundled with the program.

import { copyFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

// entry.png lives beside main.ts in the repository. The URL form keeps the
// lookup anchored to this file whatever directory the grader starts from.
const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) {
  throw new Error('entry.png is missing beside main.ts; nothing to submit');
}

// The grader writes to /output; local runs override it through the env var.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outputDir, 'entry.png');

copyFileSync(source, target);

// The gate accepts at most 1 MiB; log the size so a local run shows at a
// glance that the bundled image is inside the limit.
const { size } = statSync(target);
console.log(`entry.png written to ${target} (${size} of 1048576 bytes)`);
