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

st.title("📋 Listagem de Tarefas")

if df.empty:
    st.warning("Nenhuma tarefa encontrada.")
else:
    status = st.radio("Filtrar por status", ["Todos", "Pendente", "Em execução", "Finalizada"], horizontal=True)
    prioridade = st.radio("Filtrar por prioridade", ["Todas", "Urgente", "Alta", "Meia", "Baixa"], horizontal=True)

    if prioridade != "Todas":
        df = df[df['prioridade'] == prioridade]

    if status != "Todos":
        df = df[df['status'] == status]

    # Diccionarios con íconos
    status_icons = {
        "Pendente": "🕓 Pendente",
        "Em execução": "⚙️ Em execução",
        "Finalizada": "✅ Finalizada"
    }

    prioridade_icons = {
        "Urgente": "🔥 Urgente",
        "Alta": "🔴 Alta",
        "Meia": "🟡 Meia",
        "Baixa": "🟢 Baixa"
    }

    # Agregar columnas con íconos
    df['status'] = df['status'].map(status_icons).fillna(df['status'])
    df['prioridade'] = df['prioridade'].map(prioridade_icons).fillna(df['prioridade'])

    st.dataframe(df, use_container_width=True, hide_index=True)
