import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Wine Quality Dashboard", layout="wide")

st.title("🍷 Wine Quality Analysis Dashboard")

@st.cache_data
def load_data():
    red = pd.read_csv("winequality-red.csv")
    red["type"] = "Red"
    white = pd.read_csv("winequality-white.csv")
    white["type"] = "White"
    return pd.concat([red, white])

df = load_data()

st.sidebar.header("Filters")
wine_type = st.sidebar.selectbox("Wine Type", ["All", "Red", "White"])
if wine_type != "All":
    df = df[df["type"] == wine_type]

quality_range = st.sidebar.slider(
    "Quality Range",
    int(df.quality.min()),
    int(df.quality.max()),
    (int(df.quality.min()), int(df.quality.max()))
)

df = df[df["quality"].between(*quality_range)]

c1, c2, c3 = st.columns(3)
c1.metric("Average Quality", round(df.quality.mean(), 2))
c2.metric("Avg Alcohol %", round(df.alcohol.mean(), 2))
c3.metric("Total Samples", df.shape[0])

st.divider()

col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(df, x="quality", color="type", barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.box(df, x="quality", y="alcohol", color="type")
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig, ax = plt.subplots()
    sns.heatmap(df.drop("type", axis=1).corr(), cmap="coolwarm", ax=ax)
    st.pyplot(fig)

with col4:
    fig = px.scatter(df, x="sulphates", y="quality", color="type")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.dataframe(df)
