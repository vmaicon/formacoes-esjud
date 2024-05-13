import pandas as pd
import streamlit as st
import locale

@st.cache_data
def clean_data(df):

    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')

    # Removendo colunas nulas ou com 100% do mesmo dado
    df = df.drop(columns=['Tags','Público Det.','Natureza','Realização'])
    df.rename(columns={'Unnamed: 0':'ID'}, inplace=True)
    
    # Removendo caracteres não numerais
    regex = r"(\d+|[^\d]+)"
    df['Vagas'] = df['Vagas'].str.extract(regex, expand=False)
    df['CH'] = df['CH'].str.extract(regex, expand=False)

    # Se Vagas vier valores nulos, será preenchido automaticamente com 10
    if df['Vagas'].isnull().any():
        df['Vagas'] = df['Vagas'].fillna(value=10)
    
    # Alterando o tipo de dado
    df['Vagas'] = df['Vagas'].astype(int)
    df['CH'] = df['CH'].astype(int)
    
    # Change column type to datetime64[ns] for column: 'Início'
    df['Início'] = pd.to_datetime(df['Início'],format="%d/%m/%Y")
    df['Fim'] = pd.to_datetime(df['Fim'],format="%d/%m/%Y")

    # Nomeando os dias da semana
    df['dia_da_semana_nome_inicio'] = df['Início'].dt.strftime('%A')
    df['dia_da_semana_nome_fim'] = df['Fim'].dt.strftime('%A')

    # Nomeando os meses
    df['meses_inicio_nomeados'] = df['Início'].dt.strftime('%B')
    df['meses_fim_nomeados'] = df['Fim'].dt.strftime('%B')
    
    # Adicionar uma nova coluna para o ano do projeto pedagógico
    df['Ano do Projeto Pedagógico'] = df['Projeto Pedagógico'].str.extract(regex, expand=False).astype(int)

    return df

# df = pd.read_excel(r'dataset\\2024-05-09-emeronweb.xls')

# df_clean = clean_data(df.copy())

#df is your dataframe
# df_clean.to_csv("dataset\\planilha-08-05-2024_tratada.csv", sep=',', encoding='utf-8', index=False)

# df_clean.to_excel("dataset\\2024-05-09-emeronweb_tratada2.xlsx", index=False)