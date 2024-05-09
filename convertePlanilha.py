import pandas as pd
import streamlit as st

@st.cache_data
def clean_data(df):
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
    
    # Adicionar uma nova coluna para o ano do projeto pedagógico
    df['Ano do Projeto Pedagógico'] = df['Projeto Pedagógico'].str.extract(regex, expand=False).astype(int)

    # Novas aolunas de dia, mes e ano a partir das colunas início e fim
    df['dia_inicio'] = df['Início'].dt.day
    df['mes_inicio'] = df['Início'].dt.month
    df['ano_inicio'] = df['Início'].dt.year
    
    df['dia_fim'] = df['Fim'].dt.day
    df['mes_fim'] = df['Fim'].dt.month
    df['ano_fim'] = df['Fim'].dt.year
    
    return df

# df = pd.read_csv(r'c:\\Documentos\\projetos-git\\jupyter-notebook\\dataset\\2024-05-09-emeronweb.csv')
df = pd.read_excel(r'c:\\Documentos\\projetos-git\\jupyter-notebook\\dataset\\2024-05-09-emeronweb.xls')

df_clean = clean_data(df.copy())

#df is your dataframe
# df_clean.to_csv("c:\\Documentos\\projetos-git\\jupyter-notebook\\dataset\\planilha-08-05-2024_tratada.csv", sep=',', encoding='utf-8', index=False)

df_clean.to_excel("c:\\Documentos\\projetos-git\\jupyter-notebook\\dataset\\2024-05-09-emeronweb_tratada2.xlsx", index=False)