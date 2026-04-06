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


# Gráfico por região

region = df_filtered.groupby("region")["vehicle_count"].mean().reset_index()
region = region.sort_values("vehicle_count", ascending=False)

fig1 = px.bar(
    region,
    x="region",
    y="vehicle_count",
    title="Fluxo por Região",
    text=region["vehicle_count"].round(2)
)

fig1.update_traces(textposition='outside')

fig1.update_layout(
    yaxis=dict(range=[
        region["vehicle_count"].min() - 0.5,
        region["vehicle_count"].max() + 0.5
    ])
)

st.plotly_chart(fig1, width='stretch')


# Gráfico por hora

hour = df_filtered.groupby("hour")["vehicle_count"].mean().reset_index()

fig2 = px.line(hour, x="hour", y="vehicle_count", title="Fluxo por Hora")
st.plotly_chart(fig2, use_container_width=True)


# Impacto da chuva

fig3 = px.box(df_filtered, x="rain", y="avg_speed_kmh", title="Impacto da Chuva na Velocidade")
st.plotly_chart(fig3, use_container_width=True)


#Eventos sociais

fig4 = px.box(df_filtered, x="social_event", y="vehicle_count", title="Impacto de Eventos no Trânsito")
st.plotly_chart(fig4, use_container_width=True)


# Correlação
corr = df_filtered[["vehicle_count", "avg_speed_kmh", "bus_delay_minutes"]].corr()
fig5 = px.imshow(corr, text_auto=True, title="Correlação")
st.plotly_chart(fig5, use_container_width=True)