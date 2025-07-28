import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="PowerSquad", layout="centered")

# --- Cabeçalho com GIF ---
st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 10px;'>
        <img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNm55c2J6b2hrYWxkdzI1Zmp1c2NqNjllNXFudXY4bDkzbm1sbGhtMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/sLs8Ll8Qx51xm/giphy.gif' width='150'>
        <h1 style='margin: 0;'>Power Squad </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Funções para carregar e salvar dados ---
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
        st.success("✅ Treino registrado!")

# --- Seleção da semana para ranking ---
st.subheader("📅 Selecione a semana para ver o ranking")
hoje = datetime.today()
inicio_semana = st.date_input("Data inicial da semana", hoje - timedelta(days=hoje.weekday()))
fim_semana = inicio_semana + timedelta(days=6)

# Filtra treinos da semana selecionada
df_semana = df[(df["data"] >= pd.to_datetime(inicio_semana)) & (df["data"] <= pd.to_datetime(fim_semana))]

# Ranking semanal
st.markdown(f"### 🏆 Ranking da semana ({inicio_semana.strftime('%d/%m')} - {fim_semana.strftime('%d/%m')})")
ranking_semana = df_semana["nome"].value_counts().reset_index()
ranking_semana.columns = ["Nome", "Treinos"]
st.dataframe(ranking_semana, use_container_width=True)

# Ranking acumulado
st.markdown("### 🔥 Ranking acumulado")
ranking_total = df["nome"].value_counts().reset_index()
ranking_total.columns = ["Nome", "Treinos"]
st.dataframe(ranking_total, use_container_width=True)

# --- Área protegida para apagar treinos ---
st.markdown("---")
st.subheader("🗑️ Área restrita: apagar treino (só você)")

senha = st.text_input("Digite a senha para liberar exclusão:", type="password")

if senha == "minhasenha123":  # TROQUE para sua senha segura aqui
    if df.empty:
        st.info("Nenhum treino registrado para apagar.")
    else:
        df_display = df.reset_index()
        df_display["data"] = df_display["data"].dt.strftime("%Y-%m-%d")
        
        treino_para_apagar = st.selectbox(
            "Selecione o treino para apagar:",
            df_display.apply(lambda row: f'{row["index"]}: {row["nome"]} - {row["data"]} - {row["treino"]}', axis=1)
        )
        
        if st.button("Apagar treino selecionado"):
            idx = int(treino_para_apagar.split(":")[0])
            df = df.drop(idx).reset_index(drop=True)
            save_data(df)
            st.success("🗑️ Treino apagado com sucesso! Atualize a página para ver a mudança.")
else:
    if senha != "":
        st.error("Senha incorreta.")
