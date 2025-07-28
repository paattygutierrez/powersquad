import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Carrega os dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("treinos.csv", parse_dates=["data"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["nome", "data", "treino"])
    return df

def save_data(df):
    df.to_csv("treinos.csv", index=False)

# Cabeçalho
st.title("🏋️‍♀️ PowerSquad - Monitoramento de Treinos")

# Carrega dados
df = load_data()

# Formulário para adicionar treino
with st.form("form_treino"):
    st.subheader("Adicionar novo treino")
    nome = st.selectbox("Quem treinou?", ["Bru", "Caro", "Patty", "Sergio", "Sonia"])
    data = st.date_input("Data do treino", datetime.today())
    treino = st.text_input("Tipo de treino (opcional)", "")
    enviar = st.form_submit_button("Salvar treino")

    if enviar:
        novo_treino = pd.DataFrame([[nome, data, treino]], columns=["nome", "data", "treino"])
        df = pd.concat([df, novo_treino], ignore_index=True)
        save_data(df)
        st.success("🏃‍♂️ Treino registrado com sucesso!")

# Seletor de semana
st.subheader("📅 Selecione a semana para ver o ranking")
hoje = datetime.today()
inicio_semana = st.date_input("Data inicial da semana", hoje - timedelta(days=hoje.weekday()))
fim_semana = inicio_semana + timedelta(days=6)

# Filtro semanal
df_semana = df[(df["data"] >= pd.to_datetime(inicio_semana)) & (df["data"] <= pd.to_datetime(fim_semana))]

# Ranking semanal
st.markdown(f"### 🏆 Ranking da semana ({inicio_semana.strftime('%d/%m')} a {fim_semana.strftime('%d/%m')})")
ranking_semana = df_semana["nome"].value_counts().reset_index()
ranking_semana.columns = ["Nome", "Treinos"]
st.table(ranking_semana)

# Ranking acumulado
st.markdown("### 🔥 Ranking acumulado")
ranking_total = df["nome"].value_counts().reset_index()
ranking_total.columns = ["Nome", "Treinos"]
st.table(ranking_total)

# Histórico de treinos
st.markdown("### 📈 Histórico completo de treinos")
st.dataframe(df.sort_values("data", ascending=False))
