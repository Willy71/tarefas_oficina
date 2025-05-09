import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------------------
# Colocar nombre en la página, icono y ampliar la pantalla
st.set_page_config(
    page_title="Gestão de Tarefas",
    page_icon="📋",
    layout="wide"
)

# Scopes necesarios
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Ruta al archivo de credenciales
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]

# Clave de la hoja de cálculo (la parte de la URL después de "/d/" y antes de "/edit")
SPREADSHEET_KEY = '1oU0C2VNJSsb0psZQOYEZd7YuXX8mgqfLP8onYc-EOjU'  # Cambia esto con la clave de tu hoja
SHEET_NAME = 'Hoja 1'

# Función para autenticar
def autenticar_gspread():
    credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    cliente = gspread.authorize(credentials)
    return cliente

# Inicializar la hoja de cálculo
gc = autenticar_gspread()
spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Cargar los datos desde Google Sheets
def cargar_datos(worksheet):
    try:
        records = worksheet.get_all_records()
        if not records:
            return pd.DataFrame(columns=['id', 'data_inicio', 'tarefa', 'status', 'prioridade', 'data_fin'])
        else:
            df = pd.DataFrame(records)
            return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return pd.DataFrame(columns=['id', 'data_inicio', 'tarefa', 'status', 'prioridade', 'data_fin'])

# Cargar los datos
df_tarefas = cargar_datos(worksheet)

# Mostrar las tareas existentes en una tabla
st.subheader("Listado de Tarefas")
st.dataframe(df_tarefas, hide_index=True)

# Selección de tarea para modificar
tarefa_id = st.selectbox("Seleccionar Tarefa para Modificar", df_tarefas['id'].values)

# Filtrar la tarea seleccionada
tarefa_row = df_tarefas[df_tarefas['id'] == tarefa_id].iloc[0]

# ----------------------------------------------------------------------------------------------------------------------------------
# Formulario para modificar la tarea seleccionada
with st.form("form_modificar_tarefa"):
    tarefa = st.text_input("Tarefa", value=tarefa_row["tarefa"])

    # Opciones de Prioridad
    prioridade_opcoes = ["Importante", "Alta", "Meia", "Baixa", "Urgente"]
    prioridade_valor = tarefa_row["prioridade"]
    if prioridade_valor not in prioridade_opcoes:
        prioridade_valor = "Meia"  # Valor por defecto si hay un error
    prioridade = st.selectbox("Prioridade", prioridade_opcoes, index=prioridade_opcoes.index(prioridade_valor))

    # Opciones de Status
    status_opcoes = ["Pendente", "Em execução", "Finalizada"]
    status_valor = tarefa_row["status"]
    if status_valor not in status_opcoes:
        status_valor = "Pendente"  # Valor por defecto si hay un error
    status = st.selectbox("Status", status_opcoes, index=status_opcoes.index(status_valor))

    # Fecha de finalización
    data_fin = st.date_input("Data final", value=pd.to_datetime(tarefa_row["data_fin"], errors='coerce'))

    # Botón para enviar el formulario
    submitted = st.form_submit_button("Salvar alterações")

    # Acción cuando el formulario es enviado
    if submitted:
        # Actualización de la tarea en el DataFrame
        df_tarefas.loc[df_tarefas['id'] == tarefa_id, 'tarefa'] = tarefa
        df_tarefas.loc[df_tarefas['id'] == tarefa_id, 'prioridade'] = prioridade
        df_tarefas.loc[df_tarefas['id'] == tarefa_id, 'status'] = status
        df_tarefas.loc[df_tarefas['id'] == tarefa_id, 'data_fin'] = str(data_fin)  # Convertir a string
        
        # Actualizar Google Sheets
        for index, row in df_tarefas.iterrows():
            worksheet.update_cell(index + 2, 1, row['id'])  # Comenzamos en la fila 2 para evitar sobrescribir los encabezados
            worksheet.update_cell(index + 2, 2, row['data_inicio'])
            worksheet.update_cell(index + 2, 3, row['tarefa'])
            worksheet.update_cell(index + 2, 4, row['status'])
            worksheet.update_cell(index + 2, 5, row['prioridade'])
            worksheet.update_cell(index + 2, 6, str(row['data_fin']))  # Convertir a string


        st.success("Tarefa modificada com sucesso!")

