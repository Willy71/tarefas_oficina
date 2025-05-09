import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página
st.set_page_config(page_title="Listagem de Tarefas", page_icon="📋", layout="wide")

# Conectar com Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]
SPREADSHEET_KEY = '1oU0C2VNJSsb0psZQOYEZd7YuXX8mgqfLP8onYc-EOjU'
SHEET_NAME = 'Hoja 1'

credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_NAME)

df = pd.DataFrame(worksheet.get_all_records())

# Aplicar color a las filas según el status
def aplicar_color(status):
    if status == 'Pendente':
        return 'background-color: #ffcc00;'  # Amarillo
    elif status == 'Em execução':
        return 'background-color: #ff9900;'  # Naranja
    elif status == 'Finalizada':
        return 'background-color: #00cc00;'  # Verde
    else:
        return ''  # Si no tiene un status definido, no se aplica color

# Mostrar la tabla con estilos
st.markdown("""
<style>
    .green {background-color: #00cc00;}  /* Verde */
    .yellow {background-color: #ffcc00;}  /* Amarillo */
    .orange {background-color: #ff9900;}  /* Naranja */
    .red {background-color: #ff3333;}  /* Rojo */
</style>
""", unsafe_allow_html=True)

st.title("📋 Listagem de Tarefas")


# Convertir el DataFrame en un HTML con estilos
html = df_tarefas.to_html(classes="table table-striped", escape=False)

# Colorear las filas según el status
for i, row in df_tarefas.iterrows():
    status = row['status']
    color = aplicar_color(status)
    html = html.replace(f'<tr><td>{row["id"]}</td>', f'<tr style="{color}"><td>{row["id"]}</td>')

# Mostrar la tabla con los colores
st.markdown(html, unsafe_allow_html=True)

#=============================================================================================

if df.empty:
    st.warning("Nenhuma tarefa encontrada.")
else:
    prioridade = st.multiselect("Filtrar por prioridade", options=df['prioridade'].unique())
    status = st.multiselect("Filtrar por status", options=df['status'].unique())

    if prioridade:
        df = df[df['prioridade'].isin(prioridade)]
    if status:
        df = df[df['status'].isin(status)]

    st.dataframe(df, use_container_width=True, hide_index=True)

