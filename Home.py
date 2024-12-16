import streamlit as st
from base import obter_base, mes_em_portugues # Importa a função do arquivo base.py
from datetime import datetime
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Gestão Hope", page_icon="🌐", layout="wide")

# Título principal
st.title("Gestão Hope")

# Adicionando uma breve descrição
st.markdown("""
    <style>
        .title-text {
            color: #2F4F4F;
            font-size: 28px;
            font-weight: bold;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            cursor: pointer;
        }
        .button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

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

# Exibindo o conteúdo principal
st.write("Aqui está o conteúdo principal da página.")
