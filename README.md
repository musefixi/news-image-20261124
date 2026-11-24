# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/musefixi/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/musefixi/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world news of Tuesday 24 November 2026: the COP31 climate talks collapsing in Antalya with no deal — the first failed COP since 2009 (CNN, The Times, Le Monde); Ukraine's naval drones sinking the Russian corvette Merkury off Benghazi, Libya (Middle East Eye, NPR); President Trump warning Iran of a "very traumatic" outcome if no nuclear deal is reached (Access24); Nvidia's board unanimously reinstating Jensen Huang as CEO (AP); the Russian war death toll nearing 700,000 according to leaked data (Kyiv Independent); Bangladesh launching a typhoid vaccination drive for 50 million children (Access24); and in sport, Brentford's 4–0 win over Everton and the Commanders' 22–20 Monday Night Football win over the Bengals (AllSports, NY Post). The repository holds the picture as `entry.png` and a small Node program that copies it to `/output/entry.png`, byte for byte, every run.

## How the image was made

The picture is drawn, not photographed: `draw.py` is a deterministic Pillow program that paints the whole collage from scratch — a navy masthead ("THE WORLD TODAY", 24 November 2026), six illustrated panels in two columns (a cracked globe for the collapsed COP31 talks, a warship under a drone strike, an aircraft carrier under a warning triangle, a rising chart and chip for Nvidia, the stark 700,000 toll on a dark panel, a shield and vaccine vial for the typhoid drive), and a navy sports strip along the bottom. No network, no randomness, no stock imagery: every pixel comes from the code in this repository, using only the DejaVu fonts bundled with the system. Running `python3 draw.py` regenerates `entry.png` byte-for-byte (1024×1024, under the 1 MiB limit), which is why the same picture is what the grader receives on every run.

## Run it

```sh
# regenerate the picture from source (optional — entry.png is already bundled)
python3 draw.py

# hand the bundled picture to the grader's output directory
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ad7vmw7e&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
