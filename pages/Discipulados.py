import streamlit as st
from datetime import datetime, timedelta
from base import conectar_firebase

# Inicializa a conexão com o Firebase
try:
    db = conectar_firebase()
except Exception as e:
    st.error(f"Erro ao conectar com o Firebase: {e}")
    st.stop()

def obter_discipuladores():
    """
    Obtém a lista única de discipuladores registrados na coleção.
    """
    try:
        discipuladores_docs = db.collection("discipulados_presenca").stream()
        discipuladores = set()

        # Verificar documentos retornados
        for doc in discipuladores_docs:
            data = doc.to_dict()
            if "discipulador" in data:
                discipuladores.add(data["discipulador"])
            else:
                st.warning(f"Documento sem o campo 'discipulador': {data}")
        
        return sorted(discipuladores)
    except Exception as e:
        st.error(f"Erro ao obter discipuladores: {e}")
        return []

def obter_registros_discipulador(discipulador):
    """
    Obtém os registros de discipulados para um discipulador específico.
    """
    try:
        registros_docs = db.collection("discipulados_presenca").where("discipulador", "==", discipulador).stream()
        discipulos_data = {}
        for doc in registros_docs:
            data = doc.to_dict()["data"]
            discipulo = doc.to_dict()["discipulo"]
            
            # Atualiza com a data mais recente de encontro
            if discipulo not in discipulos_data or datetime.strptime(data, "%Y-%m-%d") > datetime.strptime(discipulos_data[discipulo], "%Y-%m-%d"):
                discipulos_data[discipulo] = data
        
        return discipulos_data
    except Exception as e:
        st.error(f"Erro ao obter registros: {e}")
        return {}

# Página de constância detalhada por discipulador
st.title("Constância de Encontros por Discipulador")

# Obter a lista de discipuladores
discipuladores = obter_discipuladores()

# Filtro de discipulador
if discipuladores:
    discipulador_selecionado = st.selectbox("Selecione o discipulador", discipuladores)

    if discipulador_selecionado:
        # Obter os registros do discipulador selecionado
        registros = obter_registros_discipulador(discipulador_selecionado)

        if registros:
            st.subheader(f"Discipulados de {discipulador_selecionado}")
            for discipulo, data in registros.items():
                data_encontro = datetime.strptime(data, "%Y-%m-%d")
                dias_passados = (datetime.now() - data_encontro).days
                
                # Definir a cor do sinal
                if dias_passados <= 15:
                    sinal = "🟢"  # Verde
                elif dias_passados <= 30:
                    sinal = "🟡"  # Amarelo
                else:
                    sinal = "🔴"  # Vermelho

                # Exibir o nome do discipulado, a data do último encontro e o sinal
                st.write(f"{sinal} **{discipulo}** - Último encontro: {data_encontro.strftime('%d/%m/%Y')}")
        else:
            st.warning(f"Nenhum registro de discipulado encontrado para {discipulador_selecionado}.")
else:
    st.warning("Nenhum discipulador encontrado.")
