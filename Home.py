import streamlit as st
from base import obter_base, mes_em_portugues, conectar_firebase # Importa a função do arquivo base.py
from datetime import datetime
import pandas as pd

# Inicializa a conexão com o Firebase
try:
    db = conectar_firebase()
except Exception as e:
    st.error(f"Erro ao conectar com o Firebase: {e}")
    st.stop()

# Configuração da página
st.set_page_config(page_title="Gestão Hope", page_icon="🌐", layout="wide")

# Função para obter aniversariantes do mês atual
def obter_aniversariantes_mes(df):
    # Garantir que a coluna de data está no formato datetime
    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors='coerce')
    
    # Filtra os aniversariantes do mês atual
    mes_atual = datetime.now().month
    aniversariantes = df[df["data_nascimento"].dt.month == mes_atual]
    return aniversariantes

# Obter aniversariantes do mês
df = obter_base()
aniversariantes_mes = obter_aniversariantes_mes(df)

# Estilizando a sidebar
st.sidebar.markdown("### 🎂 Aniversariantes do Mês 🎂")

# Seção de aniversariantes na sidebar
if not aniversariantes_mes.empty:
    for _, row in aniversariantes_mes.iterrows():
        nome = row["nome"]
        
        # Formatação da data para mostrar o mês por extenso
        mes = row["data_nascimento"].strftime("%B")  # Mês em inglês
        mes_pt = mes_em_portugues(mes)  # Substitui para português
        data_nascimento = row["data_nascimento"].strftime(f"%d de {mes_pt}")
        
        # Exibe os aniversariantes na sidebar com fundo cinza escuro e texto claro
        st.sidebar.markdown(f"""
            <div style="background-color: #555555; padding: 10px; margin: 10px 0; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h2 style="color: #ffffff;">{nome}</h2>
                <p style="font-size: 16px; color: #dddddd;">Aniversário: {data_nascimento}</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.write("Não há aniversariantes neste mês!")

# Função para obter dados faltantes do Firebase
def obter_dados_faltantes():
    """
    Obtém membros com mais de 30 dias sem encontros e retorna uma lista de dicionários com informações.
    Considera apenas o registro mais recente de cada discipulado.
    """
    try:
        # Conexão com o Firebase
        db = conectar_firebase()
        documentos = db.collection("discipulados_presenca").stream()
        
        # Dicionário para armazenar o registro mais recente por discipulador-discipulado
        registros_mais_recentes = {}
        
        for doc in documentos:
            data = doc.to_dict()
            if "discipulador" in data and "discipulo" in data and "data" in data:
                chave = (data["discipulador"], data["discipulo"])
                data_encontro = datetime.strptime(data["data"], "%Y-%m-%d")
                
                # Atualiza o registro se a data for mais recente
                if chave not in registros_mais_recentes or registros_mais_recentes[chave]["data"] < data_encontro:
                    registros_mais_recentes[chave] = {
                        "discipulador": data["discipulador"].split()[0],  # Primeiro nome
                        "discipulo": data["discipulo"].split()[0],        # Primeiro nome
                        "data": data_encontro
                    }
        
        # Filtra os discipuladores que não têm encontro dentro do prazo
        hoje = datetime.now()
        discipuladores_faltando = []

        for chave, valor in registros_mais_recentes.items():
            dias_passados = (hoje - valor["data"]).days
            if dias_passados > 30:
                discipuladores_faltando.append(valor)

        return discipuladores_faltando

    except Exception as e:
        print(f"Erro ao acessar dados: {e}")
        return []

# Obter discipuladores faltando
discipuladores_faltando = obter_dados_faltantes()

# Exibe os dados com título e lista
if discipuladores_faltando:
    st.title("Discipulados Pendentes")
    
    for discipulador in discipuladores_faltando:
        dias_passados = (datetime.now() - discipulador["data"]).days
        st.write(f"**{discipulador['discipulo']}** está a **{dias_passados}** dias sem discipulado de **{discipulador['discipulador']}**")
else:
    st.write("Não há discipuladores com falta de discipulado!")