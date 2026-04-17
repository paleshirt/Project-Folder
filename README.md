# SIA Review Pulse

SIA Review Pulse is a Streamlit dashboard for exploring Singapore Airlines customer reviews. It turns the review dataset into an interactive view of ratings, review volume over time, and keyword clouds for positive and negative feedback.

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)

## Features

- Filter reviews by published platform, review type, rating range, and date range
- See quick summary metrics such as total reviews, average rating, median rating, and positive share
- Explore rating distribution with an interactive bar chart
- Track review volume over time with a monthly trend line
- Compare keyword clouds for positive and negative reviews
- Review the latest filtered records in a searchable table

## Tech Stack

- Python
- Streamlit
- Pandas
- Altair
- WordCloud

## Project Structure

```text
.
├── app.py
├── requirements.txt
└── data/
    └── singapore_airlines_reviews.csv
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd GA_DA_SIA_Review_Dashboard
```

### 2. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The dashboard will open in your browser, usually at `http://localhost:8501`.

## Data

The app expects a CSV file at:

```text
data/singapore_airlines_reviews.csv
```

The dashboard uses the following columns:

- `published_date`
- `published_platform`
- `type`
- `rating`
- `title`
- `text`
- `helpful_votes`

If you replace the dataset, keep those column names so the app continues to work.

## Deploying To Streamlit Cloud

This app is a good fit for Streamlit Community Cloud.

1. Push the repository to GitHub.
2. Make sure `app.py`, `requirements.txt`, and `data/singapore_airlines_reviews.csv` are committed.
3. Create a new app in Streamlit Cloud and point it at the repository.
4. Set the main file path to `app.py`.
5. Deploy the app and Streamlit will install the dependencies from `requirements.txt`.

If you change the dataset path or file name, update the code in `app.py` before deploying.

## Preview

Add a screenshot here after you run the app locally and capture the dashboard. A screenshot helps the repository stand out on GitHub and gives visitors an instant view of the interface.

## Notes

- The app attempts to install `wordcloud` automatically if it is missing, but installing from `requirements.txt` first is recommended.
- If all filters are too narrow, the dashboard shows a warning when no reviews match the current selection.

## License

No license file is included in this repository yet. Add one if you want to publish or share the project more broadly.
