import pandas as pd
# Importa a função que busca e retorna o DataFrame de transações
from .data_repository import get_buy_transactions_dataframe 


def calculate_average_price(df_transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Implementa o algoritmo de cálculo do Preço Médio de Aquisição (PM).
    Responsabilidade: Lógica de Negócio e Transformação (T do ETL).
    """
    if df_transactions.empty:
        print("🛑 DataFrame vazio recebido. Impossível calcular.")
        return pd.DataFrame()

    # 1. Transformação: Cria a coluna de Custo Total por Transação
    # (Preço x Quantidade)
    df_transactions['total_cost'] = df_transactions['quantity'] * df_transactions['unit_price']
    
    # 2. Agregação: Agrupa pelo Ticker (Ativo) e soma os custos/quantidades
    # Numerador (total_cost_sum) / Denominador (total_quantity_sum)
    analysis = df_transactions.groupby('ticker').agg(
        total_cost_sum=('total_cost', 'sum'),
        total_quantity_sum=('quantity', 'sum')
    ).reset_index()
    
    # 3. Cálculo Final: PM = Custo Total / Quantidade Total
    analysis['average_price'] = analysis['total_cost_sum'] / analysis['total_quantity_sum']
    
    return analysis[['ticker', 'average_price']]

# O ponto de execução principal (main) é o orquestrador:
if __name__ == "__main__":
    print("--- INICIANDO SERVIÇO DE ANÁLISE DE PORTFÓLIO ---")
    
    # 1. EXTRAÇÃO: O serviço delega a responsabilidade de I/O ao Repositório
    df_transactions = get_buy_transactions_dataframe()
    
    # 2. TRANSFORMAÇÃO: Executa o algoritmo na lógica de serviço
    df_pm = calculate_average_price(df_transactions)
    
    if not df_pm.empty:
        print("\n📊 Resultados Finais do Serviço de Análise:")
        print(df_pm)