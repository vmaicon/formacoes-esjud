import streamlit as st
import pandas as pd
from datetime import datetime

import convertePlanilha
import uploadFile

# Montagem do layout
st.set_page_config(page_title='ESJUD em números', layout='wide')

st.header(body="ESJUD EM NÚMEROS", divider=True)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:

        upload_file = st.file_uploader("Escolha o arquivo", help="xls, xlsx")

        if upload_file is not None:

            df = pd.read_excel(upload_file)
            df_clean = convertePlanilha.clean_data(df.copy())
            st.session_state['df_clean'] = df_clean

        if 'df_clean' not in st.session_state:
            st.info("Faça upload de um arquivo")
    if 'df_clean' in st.session_state:
        with col2:
            # converte para xlsx
            xlsx_data = uploadFile.convert_df(df_clean)

            # converte para csv
            csv = uploadFile.convert_df_to_csv(df_clean)

            st.download_button(
                    label="Downlaod da planilha tratada em formato xlsx",
                    data=xlsx_data,
                    file_name=f"{datetime.now()} - file.xlsx",
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    type='primary'
                )
            
            st.download_button(
                label="Downlaod do arquivo CSV",
                data=csv,
                file_name=f"{datetime.now()} - file.csv",
                mime='text/csv',
                key='download-csv',
                type='secondary'
            )
    
        st.write(df_clean)

with st.container():
    if "df_clean" in st.session_state:
        # Métricas
        df_metricas = df_clean[['Início','Atividade','Vagas','N. Alunos','Concluintes','Não Concluintes','CH']]

        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1.container(border=True):
                st.metric(label='Vagas 📝', value=df_metricas['Vagas'].sum())
            
            with col2.container(border=True):
                st.metric(label='Número de Alunos 👥', value=df_metricas['N. Alunos'].sum())

            with col3.container(border=True):
                st.metric(label='Concluintes 🎓', value=df_metricas['Concluintes'].sum())

            with col4.container(border=True):
                st.metric(label='Carga horária 🕓', value=df_metricas['CH'].sum())

        # Gráficos:
        df_vagas_alunos_concluintes = df_metricas.drop(columns=['Início', 'Atividade','CH', 'Não Concluintes']).sum().to_frame()
        with st.container():
            col1, col2 = st.columns(2)
            with col1.bar_chart(df_vagas_alunos_concluintes):
                pass
