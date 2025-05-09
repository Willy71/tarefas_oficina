import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Modificar Tarefa", page_icon="✏️", layout="wide")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]
SPREADSHEET_KEY = '1oU0C2VNJSsb0psZQOYEZd7YuXX8mgqfLP8onYc-EOjU'
SHEET_NAME = 'Hoja 1'

credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_NAME)
dados = pd.DataFrame(worksheet.get_all_records())

st.title("✏️ Modificar Tarefa")

if dados.empty:
    st.warning("Nenhuma tarefa cadastrada.")
else:
    tarefa_id = st.selectbox("Selecione o ID da tarefa", options=dados['id'].tolist())
    tarefa_row = dados[dados['id'] == tarefa_id].iloc[0]

    with st.form("form_modificar"):
        tarefa = st.text_input("Tarefa", value=tarefa_row["tarefa"])
        prioridade_opcoes = ["Importante", "Alta", "Meia", "Baixa", "Urgente"]
    
        prioridade_valor = tarefa_row["prioridade"]
        if prioridade_valor not in prioridade_opcoes:
            prioridade_valor = "Meia"  # Valor por defecto si hay un error
    
        prioridade = st.selectbox("Prioridade", prioridade_opcoes, index=prioridade_opcoes.index(prioridade_valor))
    
        status = st.selectbox("Status", ["Pendente", "Em ejecução", "Finalizada"], index=["Pendente", "Em ejecução", "Finalizada"].index(tarefa_row["status"]))
    
        data_fin = st.date_input("Data final", value=pd.to_datetime(tarefa_row["data_fin"], errors='coerce'))
    
        submitted = st.form_submit_button("Salvar alterações")
    
        if submitted:
            # Actualizar la planilla aquí
            st.success("Tarefa modificada com sucesso!")

