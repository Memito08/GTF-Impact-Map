# GTF Impact Map

An interactive world map showing the global reach of [Global Talent Fund](https://www.globtalent.org) programs across countries. Built with OpenLayers and a Winkel Tripel projection.

## Programs displayed

- GTF BIG Talent Scholars
- GTF Olympiad Grants
- GTF Coaches

Countries are color-coded by the number of programs active:

- **3 programs** — dark navy
- **2 programs** — blue
- **1 program** — light blue

## Repository structure

```
GTF-Impact-Map/
├── index.html                        # Main application (map + UI)
├── process_data.py                   # Data processing script
├── requirements.txt                  # Python dependencies
├── data/
│   ├── program participation.csv     # Countries × programs matrix (source of truth)
│   ├── GTF BIG Talent Scholars.xlsx  # BIG Scholars by country and year
│   ├── country_websites.xlsx         # Country page URLs (globtalent.org)
│   ├── country_codes.json            # ISO3 → country label mapping
│   ├── geometry.json                 # Country polygon geometries
│   └── programData.json              # Generated — do not edit manually
```

## How data flows

```
program participation.csv ─┐
                    ├─► process_data.py ─► data/programData.json ─► index.html
GTF BIG Talent     ─┘
Scholars.xlsx
```

`programData.json` is the only generated file. Everything else is either a source file or static map data.

## Updating the data

### Adding or modifying program participation

1. Open `data/program participation.csv`
2. Each row is a country. Columns `NATIONS` and `EXCL` use `1`/`0` to indicate participation
3. Save the file
4. Run the processing script (see below)

### Adding BIG Scholars

1. Open `data/GTF BIG Talent Scholars.xlsx`
2. Add a row with columns: `Country`, `Year`, `Name`
3. Save the file
4. Run the processing script

### After editing any source file

```bash
# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Run the script
python process_data.py
```

The script will:
- Regenerate `data/programData.json`
- Print the total number of countries processed
- **Warn about any country names that don't match `country_codes.json`** (mapping errors that would prevent a country from appearing on the map)

### Country name matching

Country names in the source files must match exactly the labels in `data/country_codes.json`. If a name doesn't match, the script will suggest the closest alternatives:

```
⚠️  1 country name(s) in programData.json have NO match in country_codes.json
   • "South Sudan"  → Did you mean: South Sudan, Republic of
```

To fix a mismatch, add the correction to the `normalize_country_name()` function in [process_data.py](process_data.py#L16).

## Local development

### Prerequisites

- Python 3.9+
- A local HTTP server (needed because the map loads JSON files via `fetch`)

### Setup

```bash
# Create and activate virtual environment (Windows)
py -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start a local server
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

> The map will not work if you open `index.html` directly as a file (`file://`) — it must be served over HTTP.

## Dependencies

All frontend dependencies are loaded from CDN — no build step required.

| Library | Version | Purpose |
|---------|---------|---------|
| [OpenLayers](https://openlayers.org) | 10.6.1 | Map rendering |
| [proj4js](https://proj4js.org) | 2.9.0 | Winkel Tripel projection |
| [SheetJS](https://sheetjs.com) | 0.18.5 | Excel parsing in browser |
| [Inter](https://fonts.google.com/specimen/Inter) | — | Typography |
