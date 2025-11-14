import pandas as pd
import pytest

# Importa a função que queremos testar (o "alvo" do teste)
from src.analysis_service import calculate_average_price 

def test_average_price_calculation_success():
    """
    Teste Unitário (Caminho Feliz): Garante que o algoritmo de Preço Médio (PM) 
    calcula o valor correto para múltiplos ativos.
    """
    
    # -----------------------------------------------------
    # 1. ARRANGE (Organizar): Preparamos os dados de entrada
    # -----------------------------------------------------
    # Simula o DataFrame que o data_repository retornaria do banco de dados.
    data = {
        'ticker': ['PETR4', 'PETR4', 'BBDC4'],
        'quantity': [100, 50, 200],
        'unit_price': [30.00, 32.00, 15.00]
    }
    # Converte o dicionário em um DataFrame do Pandas.
    df_transactions = pd.DataFrame(data)
    
    # -----------------------------------------------------
    # 2. ACT (Agir): Executamos a função alvo
    # -----------------------------------------------------
    df_result = calculate_average_price(df_transactions)
    
    # -----------------------------------------------------
    # 3. ASSERT (Verificar): Checamos se o resultado está correto
    # -----------------------------------------------------
    
    # Verificação PETR4:
    # Custo Total: (100*30.00) + (50*32.00) = 3000 + 1600 = 4600
    # Quantidade Total: 100 + 50 = 150
    # Preço Médio: 4600 / 150 = 30.6666...
    
    # Filtra o DataFrame de resultado para pegar o PM de PETR4
    pm_petr4 = df_result[df_result['ticker'] == 'PETR4']['average_price'].iloc[0]
    
    # Usamos pytest.approx para comparar números de ponto flutuante (com casas decimais), 
    # pois 30.666... é uma dízima.
    assert pm_petr4 == pytest.approx(30.6666, abs=1e-4) 

    # Verificação BBDC4:
    # Custo Total: (200 * 15.00) = 3000
    # Quantidade Total: 200
    # Preço Médio: 3000 / 200 = 15.00
    pm_bbdc4 = df_result[df_result['ticker'] == 'BBDC4']['average_price'].iloc[0]
    assert pm_bbdc4 == 15.00

def test_average_price_empty_dataframe():
    """
    Teste de Borda (Edge Case): Garante que a função 
    lida corretamente com uma entrada vazia (ex: nenhum dado no banco).
    """
    # 1. ARRANGE
    # Criamos um DataFrame vazio, mas com as colunas esperadas
    df_empty = pd.DataFrame(columns=['ticker', 'quantity', 'unit_price'])
    
    # 2. ACT
    df_result_empty = calculate_average_price(df_empty)
    
    # 3. ASSERT
    # Verificamos se a função retorna um DataFrame vazio, 
    # em vez de quebrar (Ex: Erro de Divisão por Zero)
    assert df_result_empty.empty, "A função deveria retornar um DataFrame vazio se a entrada for vazia."