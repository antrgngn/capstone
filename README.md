# The Devil Wears Data

> *Because that "pile of stuff" was never *just* stuff — it was data waiting to be modeled.*

## TL;DR

I built an open, longitudinal dataset of 14 luxury fashion houses (2018‑2024) — creative directors, runway calendars, sentiment, revenue, and more — then showed how causal inference (synthetic control) can quantify the impact of Pharrell Williams at Louis Vuitton.  Clone the repo, open the R notebook, and run `make all` to reproduce every figure.

---

## Table of Contents

1. [Why This Matters](#why-this-matters)
2. [Dataset Schema](#dataset-schema)
3. [Methodology](#methodology)
4. [Repository Structure](#repository-structure)
5. [Quick‑Start](#quick-start)
6. [Reproducing the Analysis](#reproducing-the-analysis)
7. [Limitations & Roadmap](#limitations--roadmap)
8. [Citation](#citation)
9. [License](#license)
10. [Contact](#contact)

---

## Why This Matters

Fashion is a **\$1.7 T** industry that still relies on anecdotes for strategic decisions.  Data exists — scattered across runway schedules, glossy editorials, and SEC filings — but no public, research‑grade panel ties it all together.

This project delivers that missing link so that:

* **Researchers** can run time‑series and causal inference without months of scraping.
* **Students** can learn econometrics on a fun, culturally rich topic.
* **Brands & analysts** can benchmark creative decisions against measurable outcomes.

---

## Dataset Schema

| Category        | Variable                                                 | Type         | Notes                              |
| --------------- | -------------------------------------------------------- | ------------ | ---------------------------------- |
| Identity        | `house`                                                  | factor       | 14 maisons in v1.0                 |
| Time            | `year`, `season`                                         | int / factor | `season ∈ {ss, fw}`                |
| Governance      | `creative_director`, `director_years`, `director_houses` | chr / int    | Tenure + career breadth            |
| Geography       | `home_base`, `parent_group`                              | factor       | Links to HQ & conglomerate         |
| Runway Presence | `paris`, `milan`, `new_york`, `london`                   | 0/1          | Major fashion weeks                |
| Culture         | `met_gala`                                               | 0/1          | Red‑carpet signal                  |
| Outcome         | `fashion_magazine_sentiment`                             | num          | VADER compound score               |
| Finance †       | `seasonal_revenue`, `employees`                          | num          | Publicly reported, where available |

† Financial coverage currently limited to houses with public filings.  See `data/codebook.csv` for detailed metadata.

Raw CSV lives in [`data/Capstone Final Draft Data.csv`](./data). A rendered codebook is in `/docs`.

---

## Methodology

### 1 · Sentiment Pipeline

* Crawl Vogue, BOF, W, Harper’s Bazaar via Google CSE + News API.
* Extract article text with *newspaper3k*.
* Score with **VADER**; aggregate by house‑season.
* Store as tidy panel (`house × season`).

Python implementation lives in [`scripts/social_media_sentiment.py`](./scripts).  A sample notebook shows exploratory plots.

### 2 · Causal Demo

In `analysis/synth_louis_vuitton.R` I replicate the synthetic control example from the report:

```r
source("analysis/synth_louis_vuitton.R")
```

The script:

1. Converts `year + season` to half‑year time.
2. Builds a donor pool (13 houses).
3. Matches on fashion‑week presence + director tenure pre‑2023.
4. Estimates ATT of Pharrell’s appointment on magazine sentiment.

Reproduced figure:

```
Impact of Pharrell Williams at Louis Vuitton (2023‑2024)
┌───────── actual (LV) ──────┐
│                             │
└── synthetic control (LV‧) ──┘
```

---

## Repository Structure

```
├── data/                  # Raw & processed CSVs + codebook
├── scripts/               # Python crawlers & sentiment pipeline
├── analysis/              # R notebooks & .R scripts for causal work
├── docs/                  # PDF report, figures, and slides
├── assets/                # Logos & banner images
└── README.md              # You are here
```

---

## Quick Start

```bash
# 1 · Clone
$ git clone https://github.com/yourusername/devil-wears-data.git
$ cd devil-wears-data

# 2 · Set up R (≥ 4.3) & install deps
$ R -e "install.packages(c('Synth','dplyr','ggplot2','tidyr','readr'))"

# 3 · (Optional) Python sentiment pipeline
$ pip install -r requirements.txt
$ python scripts/social_media_sentiment.py  # writes data/sentiment.csv
```

A `Makefile` is included for one‑command reproduction: `make all`.

---

## Reproducing the Analysis

1. Run the sentiment pipeline (or use the pre‑computed CSV).
2. Open `analysis/synth_louis_vuitton.Rmd` and knit to HTML.
3. All figures and tables from the capstone paper will be generated under `/docs`.

---

## Limitations & Roadmap

* **Coverage**: v1.0 tracks 14 houses; goal is 30+ by 2026.
* **Sentiment Model**: VADER is fashion‑agnostic; exploring FinBERT‑style fine‑tuning.
* **Financials**: Scraping PDF annual reports to improve revenue granularity.
* **CI/CD**: Automate weekly sentiment refresh via GitHub Actions.

---

## Citation

```bibtex
@misc{nguyen2024devil,
  title  = {The Devil Wears Data},
  author = {Nguyen, An},
  year   = {2024},
  note   = {GitHub repository},
  url    = {https://github.com/yourusername/devil-wears-data}
}
```

---

## License

Released under the MIT License — see [`LICENSE`](./LICENSE).

---

## Contact

Have questions or want to collaborate?

👗 An Nguyen  ·  [an@uni.minerva.edu](mailto:an@uni.minerva.edu)  ·  [@causalnotcasual](https://www.instagram.com/causalnotcasual)

*Data is the new cerulean.*
