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

# Íconos para status
status_icons = {
    "Pendente": "🕓 Pendente",
    "Em execução": "⚙️ Em execução",
    "Finalizada": "✅ Finalizada"
}

# Íconos para prioridade
prioridade_icons = {
    "Urgente": "🔥 Urgente",
    "Alta": "🔴 Alta",
    "Meia": "🟡 Meia",
    "Baixa": "🟢 Baixa"
}

# Aplicar íconos
df["Status"] = df["status"].map(status_icons)
df["Prioridade"] = df["prioridade"].map(prioridade_icons)

# Filtros
status_opcao = st.radio("Filtrar por Status", ["Todos"] + list(status_icons.keys()), horizontal=True)
prioridade_opcao = st.radio("Filtrar por Prioridade", ["Todas"] + list(prioridade_icons.keys()), horizontal=True)

if status_opcao != "Todos":
    df = df[df["status"] == status_opcao]

if prioridade_opcao != "Todas":
    df = df[df["prioridade"] == prioridade_opcao]

# Mostrar DataFrame con íconos
st.dataframe(
    df[["id", "tarefa", "Status", "Prioridade", "data", "data_fin"]],
    column_config={
        "tarefa": "Tarefa",
        "Status": st.column_config.TextColumn("Status"),
        "Prioridade": st.column_config.TextColumn("Prioridade"),
        "data": "Data Início",
        "data_fin": "Data Fim"
    },
    hide_index=True
)
