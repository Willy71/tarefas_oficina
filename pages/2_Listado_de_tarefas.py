import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página
st.set_page_config(page_title="Listagem de Tarefas", page_icon="📋", layout="wide")

# Conectar com Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]
SPREADSHEET_KEY = '1kiXS0qeiCpWcNpKI-jmbzVgiRKrxlec9t8YQLDaqwU4'
SHEET_NAME = 'Hoja 1'

credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_NAME)

df = pd.DataFrame(worksheet.get_all_records())

st.title("📋 Listagem de Tarefas")

if df.empty:
    st.warning("Nenhuma tarefa encontrada.")
else:
    prioridade = st.multiselect("Filtrar por prioridade", options=df['prioridade'].unique())
    status = st.multiselect("Filtrar por status", options=df['status'].unique())

    if prioridade:
        df = df[df['prioridade'].isin(prioridade)]
    if status:
        df = df[df['status'].isin(status)]

    st.dataframe(df, use_container_width=True)

