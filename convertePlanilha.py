import pandas as pd
import locale

def nomear_datas(df:pd.DataFrame, nova_coluna:str, coluna_base, formato_da_data:str):
    """
    Função para formatar datas em um dataframe.

    Args:
      df: O dataframe que contém as colunas de datas.
      nova_coluna: Nome para a nova coluna
      coluna_base: Indica a coluna que será usada como base para a nova_coluna
      format_da_data: indica qual será o formato da data

    Retorna:
      O dataframe modificado com as novas colunas.
    """
    
    df[nova_coluna] = df[coluna_base].dt.strftime(formato_da_data)
    return df

def converter_para_tipo_datetime(df:pd.DataFrame, coluna:str, formato:str):
    df[coluna] = pd.to_datetime(df[coluna], format=formato)

    return df

def remove_caracteres_nao_numerais(df:pd.DataFrame, coluna:str, tipo=int, ifNull='-1h'):
    """
    Função que remove os caracteres não numerais e altera o tip da coluna em uma coluna

    Args:
        df: Dataframe com as colunas para trabalhar
        coluna: string com a coluna específica
        type: especifica o novo tipo da coluna
        ifNul: se não por um valor para nulo, será preenchido com '-1h'

    Retorna:
        O dataframe modificado com uma nova coluna do tipo inteiro
    """

    if df[coluna].isnull().any():
        df[coluna] = df[coluna].fillna(value=ifNull)
    
    regex = r"(\d+|[^\d]+)"

    df[coluna] = df[coluna].str.extract(regex, expand=False).astype(tipo)

    return df

def clean_data(df):

    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')

    # Removendo colunas nulas ou com 100% do mesmo dado
    df = df.drop(columns=['Tags','Público Det.','Natureza','Realização'])
    df.rename(columns={'Unnamed: 0':'ID'}, inplace=True)
    
    # Removendo caracteres não numerais e altera o tipo de dado da coluna
    df = remove_caracteres_nao_numerais(df=df, coluna='Vagas', tipo=int, ifNull='10')
    df = remove_caracteres_nao_numerais(df=df, coluna='CH',tipo=int)

    # Adicionar uma nova coluna para o ano do projeto pedagógico
    df = remove_caracteres_nao_numerais(df, 'Projeto Pedagógico', int)

    # Altera o tipo da coluna para o tipo data
    df = converter_para_tipo_datetime(df, 'Início', "%d/%m/%Y")
    df = converter_para_tipo_datetime(df, 'Fim', "%d/%m/%Y")

    # Nomeando os dias da semana
    df = nomear_datas(df,'dia_da_semana_nome_inicio','Início','%A')
    df = nomear_datas(df,'dia_da_semana_nome_fim','Fim','%A')

    # Nomeando os meses
    df = nomear_datas(df,'meses_inicio_nomeados','Início','%m - %B')
    df = nomear_datas(df,'meses_fim_nomeados','Fim','%m - %B')

    # Mês referência
    df = nomear_datas(df,'mes_referencia','Início','%m - %B')
    df.loc[df['Tipo de Atividade'].str.contains('AutoInstrucional'), 'mes_referencia'] = '13 - Anual'

    return df