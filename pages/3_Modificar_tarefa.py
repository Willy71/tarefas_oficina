import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Modificar Tarefa", page_icon="✏️", layout="wide")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]
SPREADSHEET_KEY = '1kiXS0qeiCpWcNpKI-jmbzVgiRKrxlec9t8YQLDaqwU4'
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

    with st.form("editar_tarefa"):
        tarefa = st.text_input("Descrição", value=tarefa_row['tarefa'])
        prioridade = st.selectbox("Prioridade", ["Importante", "Alta", "Meia", "Baixa", "Urgente"], index=["Importante", "Alta", "Meia", "Baixa", "Urgente"].index(tarefa_row['prioridade']))
        status = st.selectbox("Status", ["Pendente", "Em execução", "Finalizada"], index=["Pendente", "Em execução", "Finalizada"].index(tarefa_row['status']))
        data_inicio = st.date_input("Data início", value=pd.to_datetime(tarefa_row['data_inicio']))
        data_fin = st.date_input("Data final", value=pd.to_datetime(tarefa_row['data_fin']))
        submit = st.form_submit_button("Salvar alterações")

    if submit:
        # Atualiza no Google Sheets
        linha = dados[dados['id'] == tarefa_id].index[0] + 2  # +2 pois o índice começa em 0 e a planilha tem header na 1
        worksheet.update(f'B{linha}', [[str(data_inicio), tarefa, prioridade, status, str(data_fin)]])
        st.success("✅ Tarefa atualizada com sucesso!")
        st.experimental_rerun()

