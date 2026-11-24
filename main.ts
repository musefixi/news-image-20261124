// news-image-20261124: "Sum up 24 November's world news in one image."
//
// The picture of the day sits beside this file as entry.png. The grader
// runs this program twice in a sandbox with no network and reads only
// /output/entry.png, so the whole job here is a faithful byte-for-byte
// copy of the bundled image into the output directory.
//
// Locally, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

// Runs with no network and no dependencies: Node's standard library only.
// The image is drawn once, ahead of time, and bundled with the program.

import { copyFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) {
  throw new Error('entry.png is missing beside main.ts; nothing to submit');
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outputDir, 'entry.png');

copyFileSync(source, target);

// The gate accepts at most 1 MiB; log the size so a local run shows at a
// glance that the bundled image is inside the limit.
const { size } = statSync(target);
console.log(`entry.png written to ${target} (${size} of 1048576 bytes)`);
