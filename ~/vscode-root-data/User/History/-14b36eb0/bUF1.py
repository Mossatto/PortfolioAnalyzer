import pandas as pd
import pytest

# Importa a função que queremos testar (o "alvo" do teste)
from src.analysis_service import calculate_average_price 

def test_calculo_preco_medio_sucesso():
    """
    Teste Unitário: Garante que o algoritmo de Preço Médio (PM) 
    calcula o valor correto para múltiplos ativos.
    """
    
    # -----------------------------------------------------
    # 1. ARRANGE (Organizar): Preparamos os dados de entrada
    # -----------------------------------------------------
    # Simula o DataFrame que o data_repository retornaria
    data = {
        'ticker': ['PETR4', 'PETR4', 'BBDC4'],
        'quantity': [100, 50, 200],
        'unit_price': [30.00, 32.00, 15.00]
    }
    df_transactions = pd.DataFrame(data)
    
    # -----------------------------------------------------
    # 2. ACT (Agir): Executamos a função
    # -----------------------------------------------------
    df_resultado = calculate_average_price(df_transactions)
    
    # -----------------------------------------------------
    # 3. ASSERT (Verificar): Checamos se o resultado está correto
    # -----------------------------------------------------
    
    # Verificação PETR4:
    # Custo Total: (100*30.00) + (50*32.00) = 3000 + 1600 = 4600
    # Quantidade Total: 100 + 50 = 150
    # Preço Médio: 4600 / 150 = 30.6666...
    pm_petr4 = df_resultado[df_resultado['ticker'] == 'PETR4']['average_price'].iloc[0]
    
    # Usamos pytest.approx para comparar números de ponto flutuante (com casas decimais)
    assert pm_petr4 == pytest.approx(30.6666, abs=1e-4) 

    # Verificação BBDC4:
    # Custo Total: (200 * 15.00) = 3000
    # Quantidade Total: 200
    # Preço Médio: 3000 / 200 = 15.00
    pm_bbdc4 = df_resultado[df_resultado['ticker'] == 'BBDC4']['average_price'].iloc[0]
    assert pm_bbdc4 == 15.00

def test_calculo_preco_medio_dataframe_vazio():
    """
    Teste de Borda (Edge Case): Garante que a função 
    lida corretamente com uma entrada vazia.
    """
    # 1. ARRANGE
    df_vazio = pd.DataFrame(columns=['ticker', 'quantity', 'unit_price'])
    
    # 2. ACT
    resultado_vazio = calculate_average_price(df_vazio)
    
    # 3. ASSERT
    assert resultado_vazio.empty, "A função deveria retornar um DataFrame vazio se a entrada for vazia."