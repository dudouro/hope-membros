from base import obter_base, conectar_firebase
import pandas as pd
import streamlit as st
from datetime import datetime

# Inicializa a conexão com o Firebase
try:
    db = conectar_firebase()
except Exception as e:
    st.error(f"Erro ao conectar com o Firebase: {e}")
    st.stop()

# Obtendo a base de dados da planilha
df_base = obter_base()

# Extraindo nomes das pessoas na base de dados (supondo que a coluna é "nome")
pessoas_base = df_base["nome"].dropna().tolist()

# Função para adicionar discipulados ao Firestore
def adicionar_discipulado(nome, data, celula, discipulador):
    """
    Adiciona um discipulado ao Firestore.

    :param nome: Nome da pessoa discipulada.
    :param data: Data do discipulado.
    :param celula: Célula a que pertence.
    :param discipulador: Nome do discipulador responsável.
    """
    try:
        discipulado = {
            "nome": nome,
            "data": data,
            "celula": celula,
            "discipulador": discipulador
        }
        db.collection("discipulados").add(discipulado)
        st.success(f"Discipulado de {nome} adicionado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao adicionar discipulado: {e}")

# Interface para adicionar novos discipulados
st.subheader("Adicionar Novo Discipulado")
with st.form("form_discipulado"):
    nome = st.selectbox("Nome da Pessoa Discipulada", pessoas_base)
    data = st.date_input("Data do Discipulado", datetime.now())
    celula = st.selectbox("Célula", ["Celula 18", "Celula 14-17"])
    discipulador = st.selectbox("Nome do Discipulador", pessoas_base)

    # Botão para enviar o formulário
    enviado = st.form_submit_button("Adicionar Discipulado")
    if enviado:
        adicionar_discipulado(nome, str(data), celula, discipulador)

# Exibir discipulados que correspondem à base
st.subheader("Discipulados Cadastrados (Correspondentes à Base)")
try:
    discipulados_ref = db.collection("discipulados").stream()
    discipulados = [
        {
            "discipulador": doc.to_dict().get("discipulador", ""),
            "discipulado": doc.to_dict().get("nome", ""),
        }
        for doc in discipulados_ref
    ]

    # Filtrar discipulados cujos nomes existem na base
    discipulados_filtrados = [
        d for d in discipulados if d["discipulado"] in pessoas_base
    ]

    # Contar o total de discipulados filtrados
    total_discipulados = len(discipulados_filtrados)

    # Exibir o total e os discipulados
    st.markdown(f"### Total de Discipulados (na base): {total_discipulados}")
    if discipulados_filtrados:
        discipulados_df = pd.DataFrame(discipulados_filtrados)
        st.dataframe(discipulados_df)
    else:
        st.write("Nenhum discipulado registrado corresponde às pessoas na base.")
except Exception as e:
    st.error(f"Erro ao carregar discipulados: {e}")
