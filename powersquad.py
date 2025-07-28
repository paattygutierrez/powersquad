import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- Estilo personalizado ---
st.markdown("""
    <style>
        body {
            background-color: white !important;
            color: #111 !important;
        }
        .stApp {
            background-color: white !important;
            color: #111 !important;
        }
        h1, h2, h3, h4, h5, h6, label, div, span {
            color: #111 !important;
        }
        header, footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# --- Cabeçalho com GIF ---
st.markdown(
    """
    <h1 style="display:flex; align-items:center; gap:10px;">
        <img src="https://media.giphy.com/media/SuKXH1n6r7ZZW/giphy.gif" width="60"/>
        PowerSquad - Monitoramento de Treinos
    </h1>
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
    st.subheader("➕ Adicionar novo treino")
    nome = st.selectbox("Quem treinou?", ["Bru", "Caro", "Patty", "Sergio", "Sonia"])
    data = st.date_input("Data do treino", datetime.today())
    treino = st.text_input("Tipo de treino (opcional)", "")
    enviar = st.form_submit_button("Salvar treino")

    if enviar:
        novo_treino = pd.DataFrame([[nome, data, treino]], columns=["nome", "data", "treino"])
        df = pd.concat([df, novo_treino], ignore_index=True)
        save_data(df)
        st.success("🏃‍♀️ Treino registrado com sucesso!")

# --- Seleção de semana ---
st.subheader("📅 Selecione a semana para ver o ranking")
hoje = datetime.today()
inicio_semana = st.date_input("Data inicial da semana", hoje - timedelta(days=hoje.weekday()))
fim_semana = inicio_semana + timedelta(days=6)

# --- Filtro de dados da semana ---
df_semana = df[(df["data"] >= pd.to_datetime(inicio_semana)) & (df["data"] <= pd.to_datetime(fim_semana))]

# --- Ranking semanal ---
st.markdown(f"### 🏆 Ranking da semana ({inicio_semana.strftime('%d/%m')} a {fim_semana.strftime('%d/%m')})")
ranking_semana = df_semana["nome"].value_counts().reset_index()
ranking_semana.columns = ["Nome", "Treinos"]
st.table(ranking_semana)

# --- Ranking acumulado ---
st.markdown("### 🔥 Ranking acumulado")
ranking_total = df["nome"].value_counts().reset_index()
ranking_total.columns = ["Nome", "Treinos"]
st.table(ranking_total)

# --- Histórico completo ---
st.markdown("### 📈 Histórico de treinos")
st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)
