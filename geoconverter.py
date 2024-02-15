import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static

########################################### configuração da pagina
############################################ Largura da pagina

about_text = """
**Conversor de coordenadas Geograficas**

Bem-vindo ao nosso aplicativo! 
Estamos empolgados por você estar aqui e gostaríamos de compartilhar algumas informações sobre o que oferecemos e nosso propósito.

**Missão e Objetivo**

Nosso aplicativo foi desenvolvido com o objetivo de fornecer a você uma experiência fácil de converter suas coordenadas geograficas
que estão no formato graus, minutos e segundo para graus decimais. Esperamos que possa encontrar valor em nosso aplicativo, 
na medida
em que este possa responder as suas necessidades. Obrigado.

...

"""

instrução='''
Para poder usar o recurso de conversão, primeiro deve remover qualquer caracter especial dos seus dados, nomeadamente, o simbolo de graus (º),
o simbolo de minutos (') e o simbolo de segundos ("). Remova igualmente as letras no inicio ou no fim de cada coordenada, caso este esteja presente. Obrigado.

'''

menu_items = {
    "About": about_text,
    "Report a bug": "mailto:anhambombe@gmail.com",  # Use o formato correto para um link de e-mail
    "Get help": "https://streamlit.io/community"  # Adicione uma entrada para a página "About" em português
}


# Configure a página
st.set_page_config(
    page_title="Geoconversor",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=menu_items # Use a lista de itens de menu corretamente definida
)
#st.set_page_config(layout="wide")

# Defina a largura desejada em pixels
largura_da_pagina = 1000

def dms_to_decimal(degrees, minutes, seconds):
    decimal = degrees + minutes / 60 + seconds / 3600
    return decimal

def convert_coordinates(latitude_str, longitude_str):
    # Extrair graus, minutos e segundos da string
    lat_parts = latitude_str.split(' ')
    lat_deg = int(lat_parts[0])
    lat_min = int(lat_parts[1])
    lat_sec = int(lat_parts[2])
    
    lon_parts = longitude_str.split(' ')
    lon_deg = int(lon_parts[0])
    lon_min = int(lon_parts[1])
    lon_sec = int(lon_parts[2])
    
    # Converter para graus decimais
    latitude_decimal = dms_to_decimal(lat_deg, lat_min, lat_sec)
    longitude_decimal = dms_to_decimal(lon_deg, lon_min, lon_sec)
    
    return -latitude_decimal, longitude_decimal

st.sidebar.image("https://cdn-icons-png.flaticon.com/128/9098/9098322.png")
st.sidebar.header("Geoconversor")
st.header("🧭 Conversor de Coordenamdas Geograficas: Graus, Minutos e Segundos para Graus Decimais")
with st.sidebar.expander("Instruções"):
    st.write(instrução)
    st.image("https://cdn-icons-png.flaticon.com/128/5165/5165328.png", caption="")

# Note about the chatbot


# Ler os dados do arquivo Excel
file_path = st.sidebar.file_uploader("Selecione o arquivo Excel", type=['xlsx','xls'])
if file_path is not None:
    df = pd.read_excel(file_path, sheet_name="coord")
    prov_selected = st.sidebar.multiselect('Selecione a província:', df['Provincia'].unique(),df['Provincia'][0])
    dist_selected = st.sidebar.multiselect('Selecione o distrito:', df['Distrito'].unique(),df['Distrito'][0])
    filtered_df = df[(df['Provincia'].isin(prov_selected)) & (df['Distrito'].isin(dist_selected))]
    if len(filtered_df) > 0:
        #n = st.sidebar.number_input("Total de linhas para mostrar:", min_value=1, max_value=len(filtered_df))
        
        # Aplicar a função de conversão
        filtered_df[['Latitude_decimal', 'Longitude_decimal']] = filtered_df.apply(lambda row: convert_coordinates(row['Latitude'], row['Longitude']), axis=1, result_type='expand')

        # Criar um mapa com base na média das coordenadas
        mapa = folium.Map(location=[filtered_df['Latitude_decimal'].mean(), filtered_df['Longitude_decimal'].mean()], zoom_start=2, width='100%')

        # Adicionar marcadores para cada localização
        for index, row in filtered_df.iterrows():
            folium.Marker([row['Latitude_decimal'], row['Longitude_decimal']], popup=row['Provincia'] + ', ' + row['Distrito']).add_to(mapa)
        st.write(filtered_df.head())

        # Exibir o mapa
        folium_static(mapa)
    else:
        st.sidebar.write("Nenhum dado encontrado com")
st.sidebar.empty()
st.sidebar.empty()
st.sidebar.empty()
st.sidebar.empty()
st.sidebar.info("Desenvolvido por: **GPEI Moçambique**.")
