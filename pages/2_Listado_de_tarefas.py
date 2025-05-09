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

st.title("📋 Lista de Tarefas")

if df.empty:
    st.warning("Nenhuma tarefa encontrada.")
else:
    status_filtro = st.radio("Filtrar por status", ["Todos", "Pendente", "Em execução", "Finalizada"], horizontal=True)
    prioridade_filtro = st.radio("Filtrar por prioridade", ["Todas", "Urgente", "Alta", "Importante", "Meia", "Baixa"], horizontal=True)

    if prioridade:
        df = df[df['prioridade'].isin(prioridade)]
    if status:
        df = df[df['status'].isin(status)]

    st.dataframe(df, use_container_width=True, hide_index=True)

