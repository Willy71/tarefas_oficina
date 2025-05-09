import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import datetime

# -------------------------------------------------------------------
# CONFIGURAÇÃO INICIAL DA PÁGINA
st.set_page_config(
    page_title="Nova Tarefa",
    page_icon="📝",
    layout="wide"
)

# Remover espaço superior padrão
st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Background escuro
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: #00001a;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# CONEXÃO COM GOOGLE SHEETS

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]
SPREADSHEET_KEY = '1oU0C2VNJSsb0psZQOYEZd7YuXX8mgqfLP8onYc-EOjU'
SHEET_NAME = 'Hoja 1'

credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
gc = gspread.authorize(credentials)

columnas_ordenadas = ['id', 'data_inicio', 'tarefa', 'prioridade', 'status', 'data_fin']

def inicializar_hoja():
    try:
        spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
        try:
            worksheet = spreadsheet.worksheet(SHEET_NAME)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=100, cols=20)
            worksheet.append_row(columnas_ordenadas)
        return worksheet
    except Exception as e:
        st.error(f"Erro ao acessar planilha: {str(e)}")
        return None

def cargar_datos(worksheet):
    try:
        records = worksheet.get_all_records()
        return pd.DataFrame(records, columns=columnas_ordenadas) if records else pd.DataFrame(columns=columnas_ordenadas)
    except Exception as e:
        st.error(f"Erro ao cargar dados: {str(e)}")
        return pd.DataFrame(columns=columnas_ordenadas)

def gerar_id_unico(df):
    return int(df['id'].max() + 1) if not df.empty else 1

# -------------------------------------------------------------------
# LÓGICA PRINCIPAL

worksheet = inicializar_hoja()
if worksheet:
    existing_data = cargar_datos(worksheet)

    st.header("📌 Nova Tarefa")

    with st.form("nova_tarefa_form"):
        tarefa = st.text_input("Descrição da tarefa")
        prioridade = st.selectbox("Prioridade", ["Importante", "Alta", "Meia", "Baixa", "Urgente"])
        status = st.selectbox("Status", ["Pendente", "Em execução", "Finalizada"])
        data_inicio = st.date_input("Data de início", value=datetime.date.today())
        data_fin = st.date_input("Data final", value=datetime.date.today())
        submitted = st.form_submit_button("Salvar tarefa")

    if submitted:
        novo_id = gerar_id_unico(existing_data)
        nova_linha = [novo_id, str(data_inicio), tarefa, prioridade, status, str(data_fin)]
        try:
            worksheet.append_row(nova_linha)
            st.success("✅ Tarefa adicionada com sucesso!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erro ao salvar tarefa: {str(e)}")

