import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import numpy as np

st.set_page_config(
    page_title="Gestão de Tarefas",
    page_icon="📋",
    layout="wide"
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]
SPREADSHEET_KEY = '1oU0C2VNJSsb0psZQOYEZd7YuXX8mgqfLP8onYc-EOjU'
SHEET_NAME = 'Hoja 1'

def autenticar_gspread():
    credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    cliente = gspread.authorize(credentials)
    return cliente

gc = autenticar_gspread()
spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
worksheet = spreadsheet.worksheet(SHEET_NAME)

def cargar_datos(worksheet):
    try:
        records = worksheet.get_all_records()
        if not records:
            return pd.DataFrame(columns=['id', 'data_inicio', 'tarefa', 'status', 'prioridade', 'data_fin'])
        else:
            return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return pd.DataFrame(columns=['id', 'data_inicio', 'tarefa', 'status', 'prioridade', 'data_fin'])

df_tarefas = cargar_datos(worksheet)

st.subheader("Listado de Tarefas")
st.dataframe(df_tarefas, hide_index=True)

if not df_tarefas.empty:
    tarefa_id = st.selectbox("Seleccionar Tarefa para Modificar", df_tarefas['id'].values)
    tarefa_row = df_tarefas[df_tarefas['id'] == tarefa_id].iloc[0]

    with st.form("form_modificar_tarefa"):
        tarefa = st.text_input("Tarefa", value=tarefa_row["tarefa"])

        prioridade_opcoes = ["Urgente", "Alta", "Meia", "Baixa"]
        prioridade_valor = tarefa_row["prioridade"]
        if prioridade_valor not in prioridade_opcoes:
            prioridade_valor = "Meia"
        prioridade = st.selectbox("Prioridade", prioridade_opcoes, index=prioridade_opcoes.index(prioridade_valor))

        status_opcoes = ["Pendente", "Em execução", "Finalizada"]
        status_valor = tarefa_row["status"]
        if status_valor not in status_opcoes:
            status_valor = "Pendente"
        status = st.selectbox("Status", status_opcoes, index=status_opcoes.index(status_valor))

        data_fin = st.date_input("Data final", value=pd.to_datetime(tarefa_row["data_fin"], errors='coerce'))

        submitted = st.form_submit_button("Salvar alterações")

        if submitted:
            lista_de_todas_las_filas = worksheet.get_all_records()
            fila_encontrada = False

            for i, r in enumerate(lista_de_todas_las_filas):
                if str(r['id']) == str(tarefa_id):
                    worksheet.update_cell(i + 2, 3, str(tarefa))
                    worksheet.update_cell(i + 2, 4, str(status))
                    worksheet.update_cell(i + 2, 5, str(prioridade))
                    worksheet.update_cell(i + 2, 6, str(data_fin))
                    fila_encontrada = True
                    st.success("✅ Tarefa modificada com sucesso!")
                    break

            if not fila_encontrada:
                st.error("❌ Não foi possível localizar a tarefa para modificar.")
