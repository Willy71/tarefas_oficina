import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticación
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# Variables
SPREADSHEET_KEY = st.secrets["SPREADSHEET_KEY"]
SHEET_NAME = "tarefas"

# Cargar datos
worksheet = client.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_NAME)
data = worksheet.get_all_records()
df = pd.DataFrame(data)

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
    df[["tarefa", "Status", "Prioridade", "data", "data_fin"]],
    column_config={
        "tarefa": "Tarefa",
        "Status": st.column_config.TextColumn("Status"),
        "Prioridade": st.column_config.TextColumn("Prioridade"),
        "data": "Data Início",
        "data_fin": "Data Fim"
    },
    hide_index=True
)
