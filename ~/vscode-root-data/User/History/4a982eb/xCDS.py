import pytest
from fastapi.testclient import TestClient
from src.app import app # Importa sua instância do FastAPI
import pandas as pd

client = TestClient(app)

def test_get_all_metrics_endpoint_sucesso(mocker):
    """
    Testa o endpoint GET /api/metrics (Issue #1).
    """
    
    # 1. ARRANGE (Organizar)
    # Simula o DataFrame que o REPOSITÓRIO (get_buy_transactions_dataframe) retorna
    mock_data_raw = {
        'ticker': ['PETR4', 'PETR4', 'BBDC4'],
        'quantity': [100, 50, 200],
        'unit_price': [30.00, 32.00, 15.00]
    }
    df_mock_raw = pd.DataFrame(mock_data_raw)

    mocker.patch(
        'src.app.get_buy_transactions_dataframe', # Caminho correto do mock
        return_value=df_mock_raw
    )
    
    
    # 2. ACT (Agir)
    response = client.get("/api/metrics")
    
    # 3. ASSERT (Verificar)
    assert response.status_code == 200 
    
    response_json = response.json()
    
    # CORREÇÃO: Verifica a ordem alfabética (BBDC4 vem antes de PETR4)
    assert response_json[0]['ticker'] == 'BBDC4'
    assert response_json[0]['average_price'] == 15.00
    assert response_json[1]['ticker'] == 'PETR4'
    assert response_json[1]['average_price'] == pytest.approx(30.6666, abs=1e-4)


def test_get_all_metrics_endpoint_vazio(mocker):
    """
    Testa o tratamento de erro 404 do endpoint /api/metrics.
    """
    # 1. ARRANGE: Simula o DB retornando um DataFrame vazio
    df_vazio = pd.DataFrame(columns=['ticker', 'quantity', 'unit_price'])

    # CORREÇÃO: O mock deve interceptar a função ONDE ELA É USADA (no app.py)
    mocker.patch(
        'src.app.get_buy_transactions_dataframe', 
        return_value=df_vazio
    )
    
    # 2. ACT
    response = client.get("/api/metrics")
    
    # 3. ASSERT
    # Agora a API (corrigida) deve retornar 404
    assert response.status_code == 404 
    assert response.json() == {"detail": "Nenhuma transação encontrada para calcular métricas."}