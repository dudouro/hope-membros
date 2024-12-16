import streamlit as st
import pandas as pd
from base import obter_base


caminho_csv = "relacionamentos.csv"

# Caminho do arquivo CSV de relacionamentos
relacionamentos = pd.read_csv(caminho_csv)

# Obtém os dados principais
dados = obter_base()

st.title("Gestão de Discipuladores e Discípulos")

# Seleciona um discipulador
discipuladores = dados["nome"].unique()
discipulador_selecionado = st.selectbox("Selecione um Discipulador:", discipuladores)
discipulador_id = dados[dados["nome"] == discipulador_selecionado]["id"].values[0]

# Filtra os discípulos associados
discipulos_ids = relacionamentos[relacionamentos["discipulador_id"] == discipulador_id]["discipulado_id"]
discipulos = dados[dados["id"].isin(discipulos_ids)]

st.subheader(f"Discípulos de {discipulador_selecionado}:")
if not discipulos.empty:
    for _, row in discipulos.iterrows():
        st.write(f"- {row['nome']}")

        if st.button(f"Remover {row['nome']}", key=f"remover_{row['id']}"):
            # Remover apenas o relacionamento específico entre o discipulador e o discípulo
            relacionamentos = relacionamentos[
                (relacionamentos["discipulador_id"] != discipulador_id) |
                (relacionamentos["discipulado_id"] != row["id"])
            ]
            
            # Salvar as alterações no arquivo CSV
            relacionamentos.to_csv(caminho_csv, index=False)

            # Atualizar a interface
            st.rerun()
else:
    st.write("Nenhum discípulo associado.")

# Adicionar novo discípulo
st.subheader("Adicionar Novo Discípulo")
discipulos_disponiveis = dados[~dados["id"].isin(discipulos_ids) & (dados["id"] != discipulador_id)]
discipulado_selecionado = st.selectbox(
    "Selecione um Discípulo para Adicionar:",
    discipulos_disponiveis["nome"].values if not discipulos_disponiveis.empty else []
)

# Quando um discípulo é selecionado e o botão é clicado
if discipulado_selecionado:
    discipulado_id = dados[dados["nome"] == discipulado_selecionado]["id"].values[0]
    if st.button("Adicionar Discípulo"):
        # Adicionar o relacionamento no dataframe
        novo_relacionamento = pd.DataFrame({
            "discipulador_id": [discipulador_id],
            "discipulado_id": [discipulado_id]
        })
        relacionamentos = pd.concat([relacionamentos, novo_relacionamento], ignore_index=True)

        # Salvar as alterações no arquivo CSV
        relacionamentos.to_csv(caminho_csv, index=False)

        # Atualizar a interface
        st.rerun()

# Botão para listar as pessoas
if st.button("Listar Pessoas", key="listar_pessoas"):
    # Obtém a base de dados
    df = obter_base()
    
    # Exibe os dados na interface com uma borda e sombra estilizada
    st.write("Lista de Pessoas:")
    st.dataframe(df)
