
import pandas as pd
import os

def limpar_valores_brl(serie):
    """
    Converte valores no formato brasileiro (R$ 1.234,56) para float.
    """
    if serie.dtype == 'object' or pd.api.types.is_string_dtype(serie):
        serie = serie.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    return pd.to_numeric(serie, errors='coerce')

def carregar_dados(caminho):
    """
    Lê o CSV usando codificação e separador padrão de arquivos brasileiros.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    return pd.read_csv(caminho, encoding='Windows-1252', sep=';')

def processar_dados(df):
    """
    Realiza transformações e cálculos no DataFrame.
    """
    pd.set_option('display.max_columns', None)

    # Padronização de texto
    df['Nome do órgão superior'] = df['Nome do órgão superior'] \
        .str.upper() \
        .str.replace('MINISTÉRIO', 'MIN')

    # Conversão de valores monetários
    for col in ['Valor diárias', 'Valor passagens', 'Valor devolução', 'Valor outros gastos']:
        if col in df.columns:
            df[col] = limpar_valores_brl(df[col])

    # Criando coluna com soma
    if 'Valor diárias' in df.columns and 'Valor passagens' in df.columns:
        df['Soma duas colunas'] = df['Valor diárias'] + df['Valor passagens']

    return df

def exibir_resultados(df):
    """
    Mostra amostra e soma total de gastos.
    """
    print(df[['Valor diárias', 'Valor passagens', 'Soma duas colunas']].head(10))
    gasto_total = df['Soma duas colunas'].sum()
    print(f"\nGasto total com diárias + passagens: R$ {gasto_total:,.2f}")

if __name__ == "__main__":
    caminho_csv = os.path.join("data", "exemplo_viagem.csv")
    df_viagens = carregar_dados(caminho_csv)
    df_viagens = processar_dados(df_viagens)
    exibir_resultados(df_viagens)
