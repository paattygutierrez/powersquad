import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- Cabeçalho com GIF animado ---
st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 10px;'>
        <img src='https://media.giphy.com/media/4Z3DdOZRTcXPa/giphy.gif' width='40'>
        <h2 style='margin: 0;'>PowerSquad - Monitoramento de Treinos</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Carregamento dos dados ---
def load_data():
    try:
        df = pd.read_csv("treinos.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["nome", "data", "treino"])
        return df

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df

def save_data(df):
    df.to_csv("treinos.csv", index=False)

# --- Dados iniciais ---
df = load_data()

# --- Formulário para adicionar treino ---
with st.form("form_treino"):
    st.subheader("➕ Novo treino")
    nome = st.selectbox("Quem treinou?", ["Bru", "Caro", "Patty", "Sergio", "Sonia"])
    data = st.date_input("Data", datetime.today())
    treino = st.text_input("Tipo de treino (opcional)", "")
    enviar = st.form_submit_button("Salvar")

    if enviar:
        novo_treino = pd.DataFrame([[nome, data, treino]], columns=["nome", "data", "treino"])
        df = pd.concat([df, novo_treino], ignore_index=True)
        save_data(df)
        st.success("✅ Treino registrado!")

# --- Seleção da semana ---
st.subheader("📅 Escolha a semana")
hoje = datetime.today()
inicio_semana = st.date_input("Início da semana", hoje - timedelta(days=hoje.weekday()))
fim_semana = inicio_semana + timedelta(days=6)

# --- Filtragem semanal ---
df_semana = df[(df["data"] >= pd.to_datetime(inicio_semana)) & (df["data"] <= pd.to_datetime(fim_semana))]

# --- Ranking semanal (visual compacto) ---
st.markdown(
    f"<h4>🏆 Ranking da semana ({inicio_semana.strftime('%d/%m')} - {fim_semana.strftime('%d/%m')})</h4>",
    unsafe_allow_html=True
)
ranking_semana = df_semana["nome"].value_counts().reset_index()
ranking_semana.columns = ["Nome", "Treinos"]
st.dataframe(ranking_semana.style.set_properties(**{
    'font-size': '14px'
}), use_container_width=True)

# --- Ranking acumulado (visual compacto) ---
st.markdown("<h4>🔥 Ranking acumulado</h4>", unsafe_allow_html=True)
ranking_total = df["nome"].value_counts().reset_index()
ranking_total.columns = ["Nome", "Treinos"]
st.dataframe(ranking_total.style.set_properties(**{
    'font-size': '14px'
}), use_container_width=True)
