from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import uvicorn
import pandas as pd # Necessário para checar o resultado do DataFrame

# Importa a lógica de negócio que você já desenvolveu
from .analysis_service import calculate_average_price
from .data_repository import get_buy_transactions_dataframe # Usado para obter os dados brutos

# ---------------------------------------------------------------------
# 1. Pydantic Model: Define o formato JSON de saída da sua API
# (Garantindo que o cliente saiba o que esperar)
# ---------------------------------------------------------------------
class AssetMetric(BaseModel):
    ticker: str
    average_price: float
    
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

# ---------------------------------------------------------------------
# 4. Bloco de Execução Local (Para Testes)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Roda o servidor Uvicorn para testes locais
    uvicorn.run(app, host="0.0.0.0", port=8000)