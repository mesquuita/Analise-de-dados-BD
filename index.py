import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Leitura dos dados

df = pd.read_csv("smartcity_bigdata_dataset_50000.csv")


# Tratamento

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

df["Month"] = df["timestamp"].dt.to_period("M").astype(str)
df["hour"] = df["timestamp"].dt.hour

# Filtros

month = st.sidebar.selectbox("Selecione o mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

# MÉTRICAS

col1, col2, col3 = st.columns(3)

col1.metric("Total de Veículos", int(df_filtered["vehicle_count"].sum()))
col2.metric("Velocidade Média", round(df_filtered["avg_speed_kmh"].mean(), 2))
col3.metric("Atraso Médio Ônibus", round(df_filtered["bus_delay_minutes"].mean(), 2))


