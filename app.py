
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Spotify Music Analysis",
    page_icon="🎵",
    layout="wide"
)

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("spotify_cleaned.csv")

df = load_data()

# Title
st.title("🎵 Spotify Music Data Analysis Dashboard")
st.write("Explore Spotify songs, popularity, genres and audio features.")

# Sidebar Filters
st.sidebar.header("Filters")

genres = sorted(df["track_genre"].dropna().unique())

selected_genres = st.sidebar.multiselect(
    "Select Music Genres",
    genres,
    default=genres
)

explicit_filter = st.sidebar.selectbox(
    "Explicit Content",
    ["All", "Yes", "No"]
)

# Apply Filters
filtered_df = df[df["track_genre"].isin(selected_genres)]

if explicit_filter == "Yes":
    filtered_df = filtered_df[filtered_df["explicit"] == True]
elif explicit_filter == "No":
    filtered_df = filtered_df[filtered_df["explicit"] == False]

# Key Metrics
st.subheader("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tracks", f"{len(filtered_df):,}")
col2.metric("Average Popularity", round(filtered_df["popularity"].mean(), 2) if len(filtered_df) else 0)
col3.metric("Average Danceability", round(filtered_df["danceability"].mean(), 2) if len(filtered_df) else 0)
col4.metric("Average Energy", round(filtered_df["energy"].mean(), 2) if len(filtered_df) else 0)

if filtered_df.empty:
    st.warning("No songs found. Please change your filters.")
    st.stop()

# Graph 1: Popularity Distribution
st.subheader("1. Song Popularity Distribution")

fig1 = px.histogram(
    filtered_df,
    x="popularity",
    nbins=30,
    title="Distribution of Song Popularity"
)
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: Top Genres
st.subheader("2. Top 10 Music Genres")

genre_counts = filtered_df["track_genre"].value_counts().head(10)

fig2 = px.bar(
    x=genre_counts.index,
    y=genre_counts.values,
    labels={"x": "Genre", "y": "Number of Tracks"},
    title="Top 10 Music Genres by Tracks"
)
st.plotly_chart(fig2, use_container_width=True)

# Graph 3: Danceability vs Popularity
st.subheader("3. Danceability vs Popularity")

fig3 = px.scatter(
    filtered_df,
    x="danceability",
    y="popularity",
    color="track_genre",
    title="Danceability and Song Popularity"
)
st.plotly_chart(fig3, use_container_width=True)

# Graph 4: Energy vs Loudness
st.subheader("4. Energy vs Loudness")

fig4 = px.scatter(
    filtered_df,
    x="energy",
    y="loudness",
    title="Relationship Between Energy and Loudness"
)
st.plotly_chart(fig4, use_container_width=True)

# Graph 5: Popularity by Genre
st.subheader("5. Popularity Comparison by Genre")

top_genres = (
    filtered_df.groupby("track_genre")["popularity"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .index
)

genre_data = filtered_df[
    filtered_df["track_genre"].isin(top_genres)
]

fig5 = px.box(
    genre_data,
    x="track_genre",
    y="popularity",
    title="Popularity Distribution Across Top 10 Genres"
)
st.plotly_chart(fig5, use_container_width=True)

# Findings
st.subheader("💡 Key Findings")

st.write(
    f"- Average song popularity is "
    f"{filtered_df['popularity'].mean():.2f}."
)

st.write(
    f"- Average danceability is "
    f"{filtered_df['danceability'].mean():.2f}."
)

st.write(
    f"- Average energy is "
    f"{filtered_df['energy'].mean():.2f}."
)

st.write(
    f"- Most common genre is "
    f"{filtered_df['track_genre'].mode().iloc[0]}."
)

# Raw Data
st.subheader("📁 Explore Raw Data")

if st.checkbox("Show Raw Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

st.success("Spotify Music Analysis Dashboard Loaded Successfully!")
