import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Dashboard Avançado de Notícias", layout="wide")

st.title("Dashboard Avançado de Notícias e Análise de Sentimento")

st.sidebar.header("Filtros Avançados")

selected_sources = st.sidebar.multiselect(
    "Selecione os Portais",
    options=["G1", "CNN US", "The Guardian", "Der Spiegel", "Le Monde", "Japan Times"],
    default=[]
)

selected_sentiments = st.sidebar.multiselect(
    "Selecione o Sentimento",
    options=["positivo", "negativo", "neutro"],
    default=[]
)

st.sidebar.header("Filtro por Data")
start_date = st.sidebar.date_input("Data Inicial", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("Data Final", value=pd.to_datetime("today"))

base_url = "http://127.0.0.1:8000/stored-news"
params = {}

if selected_sources:
    params["source"] = ",".join(selected_sources)
if selected_sentiments:
    params["sentiment"] = ",".join(selected_sentiments)

params["start_date"] = start_date.strftime("%Y-%m-%d")
params["end_date"] = end_date.strftime("%Y-%m-%d")

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Erro ao buscar dados da API: {e}")
    df = pd.DataFrame()

if "created_at" not in df.columns:
    df["created_at"] = pd.to_datetime("2023-01-01") + pd.to_timedelta(range(len(df)), unit="D")

if not df.empty:
    if "source" in df.columns:
        df["source"] = df["source"].fillna("Unknown").astype(str)
    if "sentiment" in df.columns:
        df["sentiment"] = df["sentiment"].fillna("Unknown").astype(str)


total_news = df.shape[0]
st.metric("Total de Notícias", total_news)

st.markdown("---")

st.subheader("Dados das Notícias")
st.dataframe(df)

st.subheader("Distribuição de Notícias por Portal")
chart_source = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("source:N", title="Portal"),
        y=alt.Y("count()", title="Número de Notícias"),
        tooltip=["source", "count()"]
    )
    .properties(width=400, height=300)
)
st.altair_chart(chart_source, use_container_width=True)

st.subheader("Distribuição de Sentimento")
df_sentiment = df.groupby("sentiment").size().reset_index(name="count")
chart_sentiment = (
    alt.Chart(df_sentiment)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="sentiment", type="nominal"),
        tooltip=["sentiment", "count"]
    )
    .properties(width=400, height=300)
)
st.altair_chart(chart_sentiment, use_container_width=True)

st.subheader("Evolução das Notícias ao Longo do Tempo")
df_time = df.groupby("created_at").size().reset_index(name="count")
chart_time = (
    alt.Chart(df_time)
    .mark_line(point=True)
    .encode(
        x=alt.X("created_at:T", title="Data"),
        y=alt.Y("count:Q", title="Número de Notícias"),
        tooltip=["created_at", "count"]
    )
    .properties(width=800, height=300)
)
st.altair_chart(chart_time, use_container_width=True)

st.markdown("---")
st.markdown("Utilize os filtros na barra lateral para refinar os dados exibidos.")
