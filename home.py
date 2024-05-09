import streamlit as st
import pandas as pd
import plotly.express as px
import convertePlanilha

# Montagem do layout
st.set_page_config(page_title='ESJUD em números', layout='wide')

st.header(body="ESJUD EM NÚMEROS", divider=True)

with st.container():

    upload_file = st.file_uploader("Escolha o arquivo", help="xls, xlsx")

    if upload_file is not None:

        df = pd.read_excel(upload_file)
        df_clean = convertePlanilha.clean_data(df.copy())

    if 'df_clean' not in st.session_state:
            st.session_state['df_clean'] = df_clean
    
    df_clean = st.session_state['df_clean']

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

    with col2:
        fig = px.bar(df_clean,x="Vagas",y='mes_inicio',orientation="h")
        st.plotly_chart(figure_or_data=fig, use_container_width=True)


# Tabela com os dados
with st.container(border=True):
    st.dataframe(df_clean.get(["ID","Início", "Atividade", "CH", "N. Alunos"]), use_container_width=True, hide_index=True)