import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Power Squad", layout="centered")

# Cabeçalho com gif
st.markdown("""
<div style='display: flex; align-items: center; gap: 10px;'>
    <img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNm55c2J6b2hrYWxkdzI1Zmp1c2NqNjllNXFudXY4bDkzbm1sbGhtMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/sLs8Ll8Qx51xm/giphy.gif' width='150'>
    <h1 style='margin: 0;'>Power Squad</h1>
</div>
""", unsafe_allow_html=True)

def load_data():
    try:
        df = pd.read_csv("treinos.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["nome", "data", "treino"])
        return df
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data"]).reset_index(drop=True)
    return df

def save_data(df):
    df.to_csv("treinos.csv", index=False)

df = load_data()

# Cria as abas
tab1, tab2 = st.tabs(["Registro de Treino", "Visualizar Ranking"])

with tab1:
    st.header("💪 Registrar Novo Treino")
    with st.form("form_treino"):
        nome = st.selectbox("Quem treinou?", ["Bru", "Caro", "Patty", "Sergio", "Sonia"])
        data = st.date_input("Data do treino", datetime.today())
        treino = st.text_input("Tipo de treino (opcional)", "")
        enviar = st.form_submit_button("Salvar treino")

        if enviar:
            existe = ((df["nome"] == nome) & (df["data"] == pd.to_datetime(data))).any()
            if existe:
                st.warning(f"{nome} já registrou treino na data {data.strftime('%d/%m/%Y')}.")
            else:
                novo_treino = pd.DataFrame([[nome, data, treino]], columns=["nome", "data", "treino"])
                df = pd.concat([df, novo_treino], ignore_index=True)

                # Converte a coluna data para datetime para evitar erro de tipos mistos
                df["data"] = pd.to_datetime(df["data"], errors="coerce")

                save_data(df)
                st.success("✅ Treino registrado!")
    
    st.markdown("---")
    st.subheader("🗑️ Área restrita: apagar treino (só você)")
    senha = st.text_input("Digite a senha para liberar exclusão:", type="password")

    if senha == "minhasenha123":  # Troque para sua senha segura
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
        if senha:
            st.warning("Senha incorreta. Tente novamente.")

with tab2:
    st.header("🏆 Ranking dos Treinos")
    opcao_ranking = st.radio("Escolha o ranking para visualizar:", ("Ranking da semana", "Ranking acumulado"))

    if opcao_ranking == "Ranking da semana":
        hoje = datetime.today()
        inicio_semana = st.date_input("Data inicial da semana", hoje - timedelta(days=hoje.weekday()))
        fim_semana = inicio_semana + timedelta(days=6)

        inicio_semana_ts = pd.Timestamp(inicio_semana)
        fim_semana_ts = pd.Timestamp(fim_semana)

        df_filtrado = df[(df["data"] >= inicio_semana_ts) & (df["data"] <= fim_semana_ts)]

        st.markdown(f"**Ranking da semana ({inicio_semana.strftime('%d/%m')} - {fim_semana.strftime('%d/%m')})**")
        ranking = df_filtrado["nome"].value_counts().reset_index()
        ranking.columns = ["Nome", "Treinos"]
        st.dataframe(ranking, use_container_width=True)

    else:
        st.markdown("**Ranking acumulado**")
        ranking = df["nome"].value_counts().reset_index()
        ranking.columns = ["Nome", "Treinos"]
        st.dataframe(ranking, use_container_width=True)
