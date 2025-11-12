# 💰 Personal Investment Analyzer & BB Data Tracker

## 🚀 Visão Geral do Projeto

Este projeto é uma aplicação de análise de portfólio de investimentos que visa calcular métricas financeiras essenciais (custo médio, retorno, volatilidade) e simular a integração de dados financeiros (API do BACEN/B3).

O desenvolvimento utiliza uma stack alinhada às tecnologias modernas do mercado financeiro e foi concebido como parte do meu plano de estudos para o concurso do Banco do Brasil (Agente de Tecnologia).

---

## 🎯 Alinhamento com o Concurso BB (Vantagem Competitiva)

O design deste sistema foca na aplicação prática de tópicos com alto peso em concursos e processos seletivos para o setor financeiro:

* **Banco de Dados:** Aplicação de Normalização (3FN), domínio de SQL (DDL e DML) e uso do SGBD **PostgreSQL**.
* **Programação:** Lógica de *backend* em **Python** (Cálculos de Algoritmos Financeiros e manipulação de dados com Pandas).
* **Engenharia de Software:** Uso de Metodologia Ágil (Kanban/Trello), Versionamento via **Git** e documentação técnica.

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Linguagem Backend** | Python 3.x | Implementação da lógica de análise e scripts de ingestão de dados. |
| **Banco de Dados (SGBD)** | PostgreSQL | SGBD robusto e open source, amplamente utilizado em ambientes corporativos. |
| **Controle de Versão** | Git / GitHub | Versionamento de código e documentação. |
| **Gestão do Projeto** | Trello / Notion | Acompanhamento das *features* e organização do ciclo de desenvolvimento. |
| **Virtualização** (Opcional) | Docker | Para facilitar o deploy e a configuração do ambiente de desenvolvimento. |

---

## 📊 Modelagem de Dados: Estrutura (Fase Inicial)

Abaixo está o detalhe do modelo de dados inicial, projetado para garantir a **integridade referencial** e a **Normalização em 3FN** (3ª Forma Normal).

**(Aqui você colará a tabela da Modelagem da Seção 2)**

### Entidades e Relacionamentos

* **Ativo:** Entidade mestre que define o que está sendo negociado.
* **Transacao:** Entidade transacional que registra o movimento de compra/venda.
* **Relacionamento:** 1 (Ativo) possui N (Transações).

---

## ⚙️ Primeiros Passos (Setup)

1.  Clone o repositório: `git clone [link do seu repo]`
2.  Crie o ambiente virtual Python: `python -m venv venv`
3.  Instale as dependências (futuras): `pip install -r requirements.txt`
4.  Configure as variáveis de ambiente para conexão com o PostgreSQL.

**Status Atual:** Fase de Arquitetura e Modelagem Concluída. Próxima etapa: Implementação DDL no PostgreSQL.
