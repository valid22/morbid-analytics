# Morbid Analytics

> *We're all going to die. Let's look at the data.*

A data-driven, multi-page website ranking 20 causes of death from the statistically inevitable to the historically documented once — including sharks, vending machines, laughing, and one very long beard.

Built as a Quarto-adjacent project for a data science course. Deployed via GitHub Pages.

## Pages

| Page | Description |
|------|-------------|
| `index.html` | Home — site overview and navigation |
| `deaths.html` | The full ranked death list (20 causes), filterable by category |
| `analytics.html` | 4 Chart.js visualizations: bar chart, log-scale spectrum, fear vs. reality doughnuts, absurd tier comparison |
| `methodology.html` | Python pipeline, full source citation table, data limitations |

## Running locally

Just open `index.html` in a browser — no build step needed. The site uses:

- Vanilla HTML/CSS/JS
- [Chart.js 4.4](https://www.chartjs.org/) via CDN
- Google Fonts (Playfair Display, DM Mono, Syne)

## Data pipeline

```bash
pip install -r requirements.txt
python pipeline.py
```

Regenerates `data/processed.csv` from `data/raw_deaths.csv`.

## Deploying to GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Set source to `main` branch, root `/`
4. Site will be live at `https://<your-username>.github.io/<repo-name>/`

## Data sources

| Source | Used for |
|--------|----------|
| CDC WONDER / NVSS | Top causes of death, annual US counts |
| NHTSA FARS | Car crash fatalities |
| NFPA | Fire and smoke deaths |
| NOAA Lightning Safety | Lightning strike deaths |
| NTSB Aviation Database | Plane crash deaths |
| CPSC Reports | TV tip-overs, vending machines |
| IAAPA | Roller coaster deaths |
| ISAF / Florida Museum | Shark attack data |
| American Heart Association | Exercise cardiac arrests |
| CDC WISQARS | Drowning, fire ant data |

## License

MIT. Data is from public domain government sources — cite your sources, people.

---

*Submitted as a Quarto website assignment, April 2026.*
