# Registro de uso de IA

Uma entrada por sessão, da mais antiga para a mais recente. Formato e regras em `AGENTS.md`.

### 2026-10-14T15:55:00-03:00 · Antigravity (Gemini 3.8 Flash)
- **Pedido:** Inicialização do case técnico de Analytics Engineer, configuração de salvaguardas de isolamento, profiling e descoberta dos dados, teste adversarial de hipóteses, modelagem dimensional em camadas com DuckDB, testes automatizados e elaboração da apresentação executiva e documentação.
- **O que a IA fez ou sugeriu:** Clonou o repositório e criou a branch `entrega`; verificou os hashes SHA-256 do manifesto; realizou profiling com DuckDB; descobriu a necessidade de join entre `orders` e `carts` para obter `user_id`; investigou e refutou as 3 afirmações (provou que o custo do Pix é R$ 0,019 e reconciliou o erro de denominador do operador; comprovou que o breakage da migração é de 19,78% dentro da meta e identificou que o diretor confundiu expiração/resgate; demonstrou que apenas 2,9% dos usuários Pix clicaram em comunicações); estruturou modelos SQL em camadas `staging` e `marts`; desenvolveu pipeline executável (`src/pipeline.py`) e suíte de testes com 12 asserções (`tests/test_models.py`); elaborou a apresentação executiva (`reports/apresentacao_diretoria.md`) e atualizou o `README.md`.
- **O que o candidato conferiu, corrigiu ou rejeitou:** Solicitou criação de salvaguardas contra sobrescrita de instruções; exigiu verificação adversarial para checar se a IA poderia estar errada sem editar/reclonar arquivos; acompanhou a correção de query com join de tabela de operações no DuckDB; validou a robustez dos cálculos de breakage, atribuição de CRM e reconciliação financeira.
- **Arquivos criados ou alterados:**
  - Criados: `models/staging/*.sql`, `models/marts/*.sql`, `src/pipeline.py`, `tests/test_models.py`, `reports/apresentacao_diretoria.md`, `requirements.txt`, `scripts/*.py`
  - Alterados: `README.md`, `.gitignore`, `AI_LOG.md`
