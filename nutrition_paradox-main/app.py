import streamlit as st
import sqlite3
import pandas as pd
from queries import query_map

# SQLite connection
@st.cache_resource
def get_connection():
    return sqlite3.connect("C:/Users/nancy/nutrition.db")

# Streamlit UI
st.title("Nutrition Paradox Dashboard 🥗📊")
st.markdown("Explore 25 curated queries on **Obesity**, **Malnutrition**, and **Combined Trends**")

selected_query = st.selectbox("Choose a query", list(query_map.keys()))

if st.button("Run Query"):
    conn = get_connection()
    query = query_map[selected_query]
    try:
        df = pd.read_sql_query(query, conn)
        st.success("Query executed successfully!")
        st.dataframe(df)

        if not df.empty:
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) >= 1:
                st.subheader("Optional: Quick Plot")
                chart_col = st.selectbox("Select a numeric column to plot", numeric_cols)
                st.line_chart(df.set_index(df.columns[0])[chart_col])

    except Exception as e:
        st.error(f"Query execution failed: {e}")
