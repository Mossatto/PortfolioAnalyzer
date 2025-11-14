import pandas as pd
import pytest
from fastapi.testclient import TestClient
from src.app import app # Importa sua instância do FastAPI

# Cria um cliente de teste que simula requisições HTTP
client = TestClient(app)

def test_get_all_metrics_endpoint_sucesso(mocker):
    """
    Testa o endpoint GET /api/metrics (Issue #1).
    Usa 'mocker' para simular a resposta do banco de dados 
    e testar apenas a camada da API (FastAPI).
    """
    
    # -----------------------------------------------------
    # 1. ARRANGE (Organizar)
    # -----------------------------------------------------
    
    # Simula o DataFrame que esperamos que a camada de serviço retorne
    mock_data = {
        'ticker': ['PETR4', 'BBDC4'],
        'average_price': [30.5, 14.2]
    }
    
    # O 'mocker' intercepta a chamada à função 'get_buy_transactions_dataframe'
    # e a substitui pela nossa simulação.
    mocker.patch(
        'src.analysis_logic.get_buy_transactions_dataframe', 
        return_value=pd.DataFrame(mock_data) 
    )
    
    # -----------------------------------------------------
    # 2. ACT (Agir)
    # -----------------------------------------------------
    # Simula uma chamada HTTP GET para a sua API
    response = client.get("/api/metrics")
    
    # -----------------------------------------------------
    # 3. ASSERT (Verificar)
    # -----------------------------------------------------
    assert response.status_code == 200 # Verifica se a API retornou "OK"
    
    # Verifica se o JSON retornado contém os dados simulados
    response_json = response.json()
    assert response_json[0]['ticker'] == 'PETR4'
    assert response_json[0]['average_price'] == 30.5
    assert response_json[1]['ticker'] == 'BBDC4'
    assert response_json[1]['average_price'] == 14.2

def test_get_all_metrics_endpoint_vazio(mocker):
    """
    Testa o tratamento de erro 404 do endpoint /api/metrics.
    """
    # 1. ARRANGE: Simula o DB retornando um DataFrame vazio
    mocker.patch(
        'src.analysis_logic.get_buy_transactions_dataframe', 
        return_value=pd.DataFrame(columns=['ticker', 'average_price'])
    )
    
    # 2. ACT
    response = client.get("/api/metrics")
    
    # 3. ASSERT
    assert response.status_code == 404 # Verifica se a API retornou "Not Found"
    assert response.json() == {"detail": "Nenhuma transação encontrada para calcular métricas."}