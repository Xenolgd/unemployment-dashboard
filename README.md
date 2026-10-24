# Unemployment Rate Dashboard

This project is a Streamlit dashboard that analyses unemployment rate trends 
in France using open data from data.gouv.fr.

## Research question

Why do unemployment rates in France differ by sex, age group, education level, 
and unemployment duration?

## Data source

- data.gouv.fr — Activité, emploi et chômage, séries longues  
- [https://www.data.gouv.fr/datasets/activite-emploi-et-chomage-series-longues?resource_id=03c6dc89-35e9-4f1c-8d0b-aabc018cff02](https://www.data.gouv.fr/datasets/activite-emploi-et-chomage-series-longues?resource_id=03c6dc89-35e9-4f1c-8d0b-aabc018cff02)

The dataset contains annual indicators from the French Labour Force Survey, 
including unemployment rates broken down by sex, age, education level and 
other characteristics.

## How to run the project

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Data cleaning

Before running the dashboard, the raw data can be cleaned with:

```bash
python src/data_cleaning.py
```

The cleaned dataset is saved here:

```text
data/processed/unemployment_clean.csv
```

## Project structure

```text
app.py
src/analysis.py
src/charts.py
src/data_cleaning.py
data/raw/DD_EEC_SERIES_CSV_FR.zip
data/extracted/
data/processed/unemployment_clean.csv
assets/images/
README.md
requirements.txt
```

## Features

- Interactive filters for year, sex, age group, education level and unemployment duration.
- KPIs linked to the selected filters.
- Interactive Plotly charts.
- Interpretations for each main analysis.
- Data quality and limitations section.
- Key insights and next steps.