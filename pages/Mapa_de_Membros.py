import streamlit as st
import folium
from folium.plugins import MarkerCluster
from base import obter_base
from math import radians, sin, cos, sqrt, atan2
import os

# Função para calcular a distância em linha reta entre duas coordenadas (latitude, longitude) usando a fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    # Raio da Terra em km
    R = 6371.0
    
    # Convertemos as coordenadas de graus para radianos
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Diferenças de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Distância em km
    distance = R * c
    return distance

# Supondo que df seja o seu DataFrame com as colunas 'latitude', 'longitude', 'bairro' e 'nome'
df = obter_base()  # Seu código para obter os dados

# Criar o mapa centralizado em uma coordenada aproximada de Uberlândia
mapa = folium.Map(location=[-18.9126, -48.2750], zoom_start=12)  # Coordenadas de Uberlândia

# Criar o cluster para agrupar os pontos
marker_cluster = MarkerCluster().add_to(mapa)

# Adicionar as localizações dos membros
for _, row in df.iterrows():
    latitude = row["latitude"]
    longitude = row["longitude"]
    bairro = row["bairro"]
    nome = row["nome"]

    # Tamanho do marcador baseado no número de pessoas no bairro
    bairro_count = df[df['bairro'] == bairro].shape[0]
    
    # Tamanho do marcador baseado no número de pessoas no bairro
    marker_size = 10 + bairro_count  # O tamanho do marcador aumenta conforme o número de pessoas
    marker_color = 'blue' if bairro_count == 1 else 'red'  # Varia a cor do marcador
    
    # Adiciona o marcador para o cluster
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=marker_size,  # Ajusta o tamanho do marcador conforme o número de pessoas
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.6,
        popup=f"{bairro}: {bairro_count} pessoa(s)"  # Exibe o bairro e o número de pessoas
    ).add_to(marker_cluster)

# Função para adicionar a imagem como ícone no mapa
def create_image_icon(image_path, size=(30, 30)):
    # Verifica se a imagem existe no caminho especificado
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"A imagem {image_path} não foi encontrada.")
    
    # Retorna o ícone personalizado usando a imagem
    return folium.CustomIcon(
        icon_image=image_path,  # Caminho para a imagem
        icon_size=size  # Define o tamanho do ícone
    )

# Adicionar o pin da igreja com a imagem personalizada
igreja_latitude = -18.889123012810167
igreja_longitude = -48.25467285540335

# Caminho para a imagem hope.png (certifique-se de que a imagem esteja na mesma pasta ou forneça o caminho completo)
image_path = "hope.png"  # Coloque o caminho correto para a imagem

# Criar o ícone personalizado com a imagem
custom_icon = create_image_icon(image_path, size=(40, 40))

# Adicionar o marcador para a igreja
folium.Marker(
    location=[igreja_latitude, igreja_longitude],
    popup="Igreja - Localização",  # Exibe a descrição ao clicar
    icon=custom_icon
).add_to(mapa)

# Salvar o mapa em um arquivo HTML
mapa.save("mapa_presencas_uberlandia_com_imagem_igreja.html")
# Função para simular a melhor carona e calcular os 3 membros mais próximos da linha reta
def encontrar_melhores_caronas(membro_lat, membro_lon):
    distances = []
    
    # Calcula as distâncias dos membros à linha reta entre o membro escolhido e a igreja
    for _, row in df.iterrows():
        if row["latitude"] != membro_lat or row["longitude"] != membro_lon:
            distance_to_igreja = haversine(membro_lat, membro_lon, igreja_latitude, igreja_longitude)
            distance_to_member = haversine(membro_lat, membro_lon, row["latitude"], row["longitude"])
            distances.append((row["nome"], distance_to_member, row["latitude"], row["longitude"]))
    
    # Ordena pela distância mais próxima
    distances.sort(key=lambda x: x[1])
    
    return distances[:3]

# Exibir no Streamlit
st.markdown("### Mapa das Pessoas")
st.components.v1.html(open("mapa_presencas_uberlandia_com_imagem_igreja.html", 'r').read(), height=600)

# Exibir opção de escolher o membro para procurar a carona
membro_escolhido = st.selectbox('Escolha um membro para procurar a carona', df['nome'].values)

# Obter as coordenadas do membro escolhido
membro_row = df[df['nome'] == membro_escolhido].iloc[0]
membro_latitude = membro_row['latitude']
membro_longitude = membro_row['longitude']

# Calcular os 3 membros mais próximos à linha reta
melhores_carona = encontrar_melhores_caronas(membro_latitude, membro_longitude)

# Exibir os 3 melhores membros para a carona
st.markdown(f"### Melhores Caronas para {membro_escolhido}")
for i, carona in enumerate(melhores_carona, 1):
    st.markdown(f"{i}. **{carona[0]}** - Distância: {carona[1]:.2f} km")

# Salvar o mapa em um arquivo HTML
mapa.save("mapa_presencas_uberlandia_com_imagem_igreja.html")


