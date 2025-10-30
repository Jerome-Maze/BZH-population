import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Simple Data Explorer", layout="wide")
st.title("Simple Data Explorer")

# Sidebar controls
st.sidebar.header("Data source")
uploaded = st.sidebar.file_uploader("Upload a CSV", type=["csv"])
use_demo = st.sidebar.checkbox("Use demo data", value=not uploaded)

@st.cache_data
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)

@st.cache_data
def make_demo(n=200) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "x": np.arange(n),
        "value": rng.normal(loc=0, scale=1, size=n).cumsum(),
        "category": rng.choice(["A", "B", "C"], size=n)
    })
    return df

# Load data
if uploaded and not use_demo:
    try:
        df = load_csv(uploaded)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()
else:
    n = st.sidebar.slider("Demo rows", 50, 2000, 200, step=50)
    df = make_demo(n)

st.sidebar.markdown("---")
st.sidebar.header("Plot")
numeric_cols = df.select_dtypes(include="number").columns.tolist()
if not numeric_cols:
    st.warning("No numeric columns available to plot.")
    st.dataframe(df)
    st.stop()

x_col = st.sidebar.selectbox("X column", options=numeric_cols, index=0)
y_col = st.sidebar.selectbox("Y column", options=numeric_cols, index=min(1, len(numeric_cols)-1))
agg_func = st.sidebar.selectbox("Chart type", ["Line", "Scatter", "Histogram"])

# Main layout
left, right = st.columns((3, 1))
with left:
    st.subheader("Dataset preview")
    st.dataframe(df.head(100))

    st.subheader("Plot")
    if agg_func == "Line":
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X(x_col, type="quantitative"),
            y=alt.Y(y_col, type="quantitative"),
            color="category:N" if "category" in df.columns else alt.value("#1f77b4")
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    elif agg_func == "Scatter":
        chart = alt.Chart(df).mark_circle(size=60, opacity=0.6).encode(
            x=alt.X(x_col, type="quantitative"),
            y=alt.Y(y_col, type="quantitative"),
            color="category:N" if "category" in df.columns else alt.value("#1f77b4"),
            tooltip=list(df.columns)
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:  # Histogram
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(y_col, bin=alt.Bin(maxbins=60)),
            y='count()',
            color="category:N" if "category" in df.columns else alt.value("#1f77b4"),
            tooltip=['count()']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

with right:
    st.subheader("Summary")
    st.write("Rows:", len(df))
    st.write("Columns:", len(df.columns))
    st.write("Numeric columns:", numeric_cols)
    st.write("Descriptive stats")
    st.table(df[numeric_cols].describe().T)
