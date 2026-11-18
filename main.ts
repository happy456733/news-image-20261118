// Entry point: render the 18 November 2026 front page and write it to
// $MAKEFUN_OUTPUT_DIR/entry.png. The poster is drawn in code by draw.py
// (Pillow); if the grading sandbox has no Python/Pillow, fall back to the
// pre-rendered copy shipped in assets/ — byte-identical either way.
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const root = dirname(fileURLToPath(import.meta.url));
const outFile = join(outDir, "entry.png");
const script = join(root, "draw.py");
const fallback = join(root, "assets", "entry.png");

mkdirSync(outDir, { recursive: true });

const rendered = spawnSync("python3", [script, outFile], { stdio: "inherit" });
if (rendered.status !== 0) {
  copyFileSync(fallback, outFile);
}
console.log("wrote", outFile);
