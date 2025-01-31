import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configuração da página
st.set_page_config(page_title="Dashboard de Notícias", layout="wide")

st.title("Dashboard de Notícias e Análise de Sentimento")

# Sidebar: Filtros para o usuário
st.sidebar.header("Filtros")
selected_source = st.sidebar.selectbox("Portal",
                                    options=["", "G1", "UOL", "CNN", "Oeste"],
                                    index=0)
                   
selected_sentiment = st.sidebar.selectbox(
    "Sentimento",
    options=["", "positivo", "negativo", "neutro"],
    index=0
)

# Construir a URL da API com os parâmetros de query (se houver)
base_url = "http://127.0.0.1:8000/stored-news"
params = {}
if selected_source:
    params["source"] = selected_source
if selected_sentiment:
    params["sentiment"] = selected_sentiment

# Buscar os dados da API
try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Erro ao buscar dados da API: {e}")
    df = pd.DataFrame()

# Exibir métricas
if not df.empty:
    total_news = df.shape[0]
    st.metric("Total de Notícias", total_news)
else:
    st.metric("Total de Notícias", 0)

st.markdown("---")

# Exibir os dados em tabela
st.subheader("Dados das Notícias")
st.dataframe(df)

# Se houver dados, criar gráficos com Altair
if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Notícias por Portal")
        chart1 = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("source:N", title="Portal"),
                y=alt.Y("count()", title="Número de Notícias"),
                tooltip=["source", "count()"]
            )
            .properties(width=400, height=300)
        )
        st.altair_chart(chart1, use_container_width=True)
    with col2:
        st.subheader("Notícias por Sentimento")
        chart2 = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("sentiment:N", title="Sentimento"),
                y=alt.Y("count()", title="Número de Notícias"),
                tooltip=["sentiment", "count()"]
            )
            .properties(width=400, height=300)
        )
        st.altair_chart(chart2, use_container_width=True)

st.markdown("---")
st.markdown("Use os filtros na barra lateral para refinar os dados exibidos.")
