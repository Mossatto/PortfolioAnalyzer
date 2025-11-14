from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, ConfigDict
import uvicorn
import pandas as pd # Necessário para checar o resultado do DataFrame

# Importa a lógica de negócio que você já desenvolveu
from .analysis_logic import calculate_average_price, get_metrics_for_ticker
from .data_repository import get_buy_transactions_dataframe # Usado para obter os dados brutos

# ---------------------------------------------------------------------
# 1. Pydantic Model: Define o formato JSON de saída da sua API
# (Garantindo que o cliente saiba o que esperar)
# ---------------------------------------------------------------------
class AssetMetric(BaseModel):
    ticker: str
    average_price: float
    model_config = ConfigDict(from_attributes=True)
    
    # Configuração Pydantic (Permite a criação a partir de atributos de objetos)
    class Config:
        from_attributes = True

# ---------------------------------------------------------------------
# 2. Configuração do FastAPI
# ---------------------------------------------------------------------
app = FastAPI(
    title="Portfolio Analyzer API",
    version="1.0.0",
    description="API de alta performance para cálculo de métricas financeiras."
)

# ---------------------------------------------------------------------
# 3. Endpoint: GET /api/metrics (Retorna todas as métricas)
# ---------------------------------------------------------------------

@app.get("/api/metrics", response_model=List[AssetMetric])
def get_all_metrics():
    """
    Executa a análise de Preço Médio (PM) em todos os ativos e retorna o resultado.
    """
    
    # 1. Extração dos Dados (Delega a responsabilidade ao Repositório)
    df_transactions = get_buy_transactions_dataframe()

    # 2. Execução da Lógica de Negócio (Serviço)
    df_metrics = calculate_average_price(df_transactions)

    # 3. Tratamento de Erro (Se o DB estiver vazio)
    if df_metrics.empty:
        raise HTTPException(status_code=404, detail="Nenhuma transação encontrada para calcular métricas.")

    # 4. Converte o DataFrame Pandas para o formato JSON exigido pelo Pydantic/FastAPI
    return df_metrics.to_dict('records')

@app.get("/api/metrics/{ticker}", response_model=AssetMetric)
def get_single_ticker_metrics(ticker: str):
    """
    Calcula e retorna o Preço Médio (PM) para um Ticker específico.
    Demonstra o uso de parâmetros de URL e proteção contra SQLi.
    """
    
    # 1. Validação simples (Pydantic fará mais)
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker não fornecido.")
        
    # 2. Chama o serviço de análise
    df_metric = get_metrics_for_ticker(ticker.upper()) # Converte para maiúsculas

    # 3. Tratamento de Erro (Ativo não encontrado)
    if df_metric.empty:
        raise HTTPException(status_code=404, detail=f"Nenhuma transação 'BUY' encontrada para o ticker {ticker}.")

    # 4. Retorna o primeiro (e único) resultado
    # .to_dict('records')[0] converte a primeira linha do DataFrame em um dicionário
    return df_metric.to_dict('records')[0]
# ---------------------------------------------------------------------
# 4. Bloco de Execução Local (Para Testes)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Roda o servidor Uvicorn para testes locais
    uvicorn.run(app, host="0.0.0.0", port=8000)