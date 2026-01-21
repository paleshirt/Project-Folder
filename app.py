import pandas as pd
import altair as alt
import streamlit as st
import sys
import subprocess


def ensure_wordcloud():
    try:
        from wordcloud import WordCloud, STOPWORDS
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "wordcloud"])
        from wordcloud import WordCloud, STOPWORDS
    return WordCloud, STOPWORDS

st.set_page_config(page_title="SIA Review Pulse", page_icon="✈️", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/singapore_airlines_reviews.csv")
    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce", utc=True)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["date"] = df["published_date"].dt.date
    return df


df = load_data()

st.title("SIA Review Pulse")
st.caption("Sentiment and ratings snapshot for Singapore Airlines reviews.")

st.sidebar.header("Filters")

platform_options = ["All"] + sorted(df["published_platform"].dropna().unique().tolist())
selected_platform = st.sidebar.selectbox("Platform", platform_options)

review_type_options = ["All"] + sorted(df["type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Review Type", review_type_options)

min_rating = int(df["rating"].min()) if df["rating"].notna().any() else 1
max_rating = int(df["rating"].max()) if df["rating"].notna().any() else 5
rating_range = st.sidebar.slider("Rating Range", min_rating, max_rating, (min_rating, max_rating))

min_date = df["date"].min()
max_date = df["date"].max()
default_end_date = max_date
default_start_date = (pd.Timestamp(max_date) - pd.DateOffset(months=12)).date()
default_start_date = max(min_date, default_start_date)
start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", default_end_date)

filtered = df.copy()
if selected_platform != "All":
    filtered = filtered[filtered["published_platform"] == selected_platform]
if selected_type != "All":
    filtered = filtered[filtered["type"] == selected_type]

filtered = filtered[filtered["rating"].between(rating_range[0], rating_range[1], inclusive="both")]

if start_date and end_date:
    start_date, end_date = sorted([start_date, end_date])
    filtered = filtered[(filtered["date"] >= start_date) & (filtered["date"] <= end_date)]

if filtered.empty:
    st.warning("No reviews match the current filters.")
    st.stop()

avg_rating = filtered["rating"].mean()
positive_share = (filtered["rating"] >= 4).mean() * 100
negative_share = (filtered["rating"] <= 2).mean() * 100
summary_text = (
    f"{len(filtered):,} reviews in view | "
    f"Avg rating: {avg_rating:.2f} | "
    f"Positive (4-5): {positive_share:.1f}% | "
    f"Negative (1-2): {negative_share:.1f}%"
)
st.markdown(summary_text)

overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
with overview_col1:
    st.metric("Total Reviews", f"{len(filtered):,}")
with overview_col2:
    st.metric("Average Rating", f"{avg_rating:.2f}")
with overview_col3:
    median_rating = filtered["rating"].median()
    st.metric("Median Rating", f"{median_rating:.1f}")
with overview_col4:
    st.metric("4+ Rating Share", f"{positive_share:.1f}%")

st.subheader("Rating Distribution")
ratings_chart = (
    alt.Chart(filtered.dropna(subset=["rating"]))
    .mark_bar(color="#0F4C81")
    .encode(
        x=alt.X("rating:O", title="Rating"),
        y=alt.Y("count():Q", title="Reviews"),
        tooltip=["rating:O", "count():Q"],
    )
)
st.altair_chart(ratings_chart, use_container_width=True)

st.subheader("Review Volume Over Time")
trend = (
    filtered.dropna(subset=["published_date"])
    .set_index("published_date")
    .resample("M")
    .size()
    .reset_index(name="reviews")
)
trend_chart = (
    alt.Chart(trend)
    .mark_line(point=True, color="#F59E0B")
    .encode(
        x=alt.X("published_date:T", title="Month"),
        y=alt.Y("reviews:Q", title="Reviews"),
        tooltip=["published_date:T", "reviews:Q"],
    )
)
st.altair_chart(trend_chart, use_container_width=True)

st.subheader("Keyword Clouds")
WordCloud, STOPWORDS = ensure_wordcloud()
custom_stopwords = {
    "flight",
    "flights",
    "airline",
    "airlines",
    "singapore",
    "sia",
    "would",
    "also",
    "one",
}
stopwords = STOPWORDS.union(custom_stopwords)


def build_review_text(frame):
    text_series = frame[["title", "text"]].fillna("").agg(" ".join, axis=1)
    return " ".join(text_series.tolist()).strip()


cloud_col1, cloud_col2 = st.columns(2)

with cloud_col1:
    st.markdown("**Positive Reviews (4-5)**")
    positive_reviews = filtered[filtered["rating"].between(4, 5, inclusive="both")]
    positive_text = build_review_text(positive_reviews)
    if positive_text:
        positive_cloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            stopwords=stopwords,
            collocations=False,
        ).generate(positive_text)
        st.image(positive_cloud.to_array(), use_column_width=True)
    else:
        st.info("No positive review text available for the current filters.")

with cloud_col2:
    st.markdown("**Negative Reviews (1-2)**")
    negative_reviews = filtered[filtered["rating"].between(1, 2, inclusive="both")]
    negative_text = build_review_text(negative_reviews)
    if negative_text:
        negative_cloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            stopwords=stopwords,
            collocations=False,
        ).generate(negative_text)
        st.image(negative_cloud.to_array(), use_column_width=True)
    else:
        st.info("No negative review text available for the current filters.")

st.subheader("Recent Reviews")
columns_to_show = ["published_date", "published_platform", "type", "rating", "title", "text", "helpful_votes"]
st.dataframe(
    filtered.sort_values("published_date", ascending=False)[columns_to_show].head(20),
    use_container_width=True,
)
