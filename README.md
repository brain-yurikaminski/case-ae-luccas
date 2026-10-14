# Case Analytics Engineer · Brain003 — Programa Pontua+
**Candidato:** Lucas Oliveira  
**Branch de Entrega:** `entrega`  
**Stack Técnica:** SQL / DuckDB / Python 3.9+ / Pytest  
**Tempo de Trabalho:** ~2h45 (dentro do limite sugerido de 4h)  

---

## 🚀 Guia de Reprodução Rápida (Execução Ponta a Ponta)

Este projeto foi construído para ser 100% reproduzível sem necessidade de configuração manual ou banco de dados externo.

### 1. Pré-requisitos
* Python 3.9 ou superior instalado.

### 2. Passo a Passo de Execução

```bash
# 1. Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o pipeline de transformação e modelagem (Staging + Marts)
python3 src/pipeline.py

# 4. Execute a suíte de testes automatizados de qualidade e reconciliação
pytest tests/test_models.py -v
```

Ao rodar o comando `python3 src/pipeline.py`, todos os modelos SQL serão executados sobre os dados brutos de `dados/`, o banco analítico `output/pontua_plus.duckdb` será gerado e os arquivos CSV dos marts serão exportados para `output/`.

---

## 🏛️ Arquitetura e Modelagem Dimensional

A arquitetura do projeto segue o padrão dimensional e em camadas de Analytics Engineering:

```
dados/ (Raw CSVs)
   │
   ▼
models/staging/ (Limpeza, tipagem, padronização e deduplicação)
   ├── stg_orders.sql               (Grão: order_id)
   ├── stg_order_items.sql          (Grão: order_item_id)
   ├── stg_carts.sql                (Grão: cart_id)
   ├── stg_cards.sql                (Grão: account_id)
   ├── stg_points_ledger.sql        (Grão: movement_id)
   ├── stg_crm_events.sql           (Grão: 1 evento de engajamento)
   └── stg_relatorio_mensal.sql     (Grão: mes)
   │
   ▼
models/marts/ (Tabelas Fato e Dimensões de Negócio)
   ├── fct_order_items.sql          (Grão: order_item_id - Fato transacional enriquecida)
   ├── fct_monthly_redemptions.sql  (Grão: mes - Fato agregada mensal de resgates e metas)
   ├── fct_pix_reconciliation.sql   (Grão: mes - Reconciliação do cálculo do operador)
   ├── fct_crm_attribution.sql      (Grão: user_id - Fato de atribuição da campanha Pix)
   └── fct_breakage_analysis.sql    (Grão: escopo_analise - Análise de breakage e expiração)
```

### Grãos Declarados de Cada Modelo:
* **`stg_orders`**: 1 linha por `order_id`. Contém 19.785 pedidos únicos.
* **`stg_order_items`**: 1 linha por `order_item_id`. Contém 19.803 itens.
* **`stg_carts`**: 1 linha por `cart_id`. Contém o mapeamento essencial de `cart_id` $\rightarrow$ `user_id` e canal de compra.
* **`stg_cards`**: 1 linha por `account_id` / cartão.
* **`stg_points_ledger`**: 1 linha por `movement_id`. Movimentações financeiras de crédito e débito no saldo.
* **`fct_order_items`**: 1 linha por `order_item_id`. Fato transacional de resgate enriquecida com usuário, canal, classe de cartão e status normalizado.
* **`fct_monthly_redemptions`**: 1 linha por mês (`mes`). Métricas consolidadas de volume em pontos, valores em reais, shares e avaliação das metas de Aéreas e Varejo.
* **`fct_pix_reconciliation`**: 1 linha por mês pós-Pix (`mes`). Reconciliação das ordens aprovadas vs. intenções brutas reportadas pelo operador.
* **`fct_crm_attribution`**: 1 linha por `user_id` que resgatou Pix. Mapeamento de jornada de engajamento (timing, recebimento, abertura e clique).
* **`fct_breakage_analysis`**: 1 linha por escopo conceitual de cálculo de breakage.

---

## 📖 Entendimento dos Dados e Descobertas Estruturais

A fase de profiling inicial revelou particularidades cruciais que sustentaram a modelagem:

1. **`orders.csv` não possui `user_id` preenchido:**
   * A coluna `orders.user_id` é 100% nula.
   * **Solução de Modelagem:** O relacionamento com o cliente foi recuperado através do join `orders.cart_id = carts.cart_id`, onde `carts.user_id` é 100% íntegro (6.325 usuários distintos mapeados).
2. **Classificação das Categorias em `order_items`:**
   * `category_macro = 'Aereas'` e `product_type = 'PASSAGEM'` $\rightarrow$ Passagens aéreas de parceiros (Céu Azul, Voa Linhas Aéreas, RotaSul).
   * `category_macro = 'Varejo'` e `product_type IN ('PRODUTO', 'TRANSFERENCIA')` $\rightarrow$ Produtos físicos e transferências para parceiros do grupo (Casa&Cia, MegaMagazine, Decola Viagens, Nuvem Recompensas).
   * `category_macro = 'Cashback'` e `product_type = 'TRANSFERENCIA'` $\rightarrow$ **Pontos no Pix** (fornecedor `Pix Pontua+`).
   * `category_macro = 'Cashback'` e `product_type = 'COMPRA_PONTOS'` $\rightarrow$ Aquisição de pontos via cartão/moeda.
3. **Status dos Pedidos:**
   * As análises de resgates contratuais e financeiros consideram apenas pedidos com status `APROVADO` e `FINALIZADO_COM_SUCESSO`. Pedidos `CANCELADO`, `ESTORNADO` e `INVALIDO` têm pontos devolvidos e nenhum desembolso financeiro associado.

---

## 🎯 Avaliação das Três Afirmações

### 1. Afirmação do CRM: *"A comunicação de lançamento explica o sucesso do Pix"*
* **Veredito:** ❌ **FALSA / NÃO SE SUSTENTA NOS DADOS.**
* **Evidências:**
  * O Pix foi lançado em **27/05/2026**. A primeira e única campanha de email (`CMP_LANCAMENTO_PIX_4dbee001e6aba1eb57b512c3`) só começou a ser disparada em **28/05/2026 às 13:00**. Usuários já haviam resgatado Pix antes do envio.
  * Dos **2.140 clientes únicos** que resgataram Pix, **apenas 39 clientes (1,8%) clicaram no email**.
  * Mesmo incluindo as campanhas de Push disparadas na madrugada de 28/05 (`CMP_cde3c1b2f2e76a6ea2e641d6` e `CMP_cb21c575fee7cf8fb08bed6b`), apenas **63 clientes (2,9%)** converteram após clicar em alguma notificação.
  * Mais de **64,3% dos clientes Pix resgataram de forma estritamente orgânica** sem nenhuma impressão ou clique de campanha.
  * A coluna `control_group` no CRM é 100% nula (nenhum grupo de controle foi implementado para medir incrementalidade causal).

### 2. Afirmação do Operador: *"Na verdade o Pix sai a cerca de R$ 0,016 por ponto, abaixo dos R$ 0,019 anunciados"*
* **Veredito:** ❌ **FALSA (Erro grosseiro de cálculo do operador).**
* **Evidências:**
  * No sistema transacional (`order_items`), **cada ponto em pedidos aprovados foi liquidado a EXATAMENTE R$ 0,019000** em todos os meses (média ponderada = 0,019).
  * **O Erro do Operador:** No arquivo `relatorio_mensal_cliente.csv`, a coluna `pix_pontos` contém a **soma de todos os pontos solicitados, inclusive pedidos CANCELADOS, ESTORNADOS e INVÁLIDOS** (onde nenhum real foi pago). Já a coluna `pix_reais` contém apenas o valor dos pedidos Aprovados.
  * Em Junho/2026:
    * Aprovados: 704 pedidos | 9.215.135 pts | R$ 175.087,95 $\rightarrow$ **R$ 0,019/pt**.
    * Cancelados/Inválidos/Estornados: 118 pedidos | 1.494.284 pts | R$ 0 pago.
    * Denominador do Relatório: 10.709.419 pts brutos.
    * Razão calculada pelo operador: $\frac{\text{R\$ } 174.261,75}{10.709.419 \text{ pts}} = \mathbf{0,016272}$.
  * O custo efetivo unitário do Pix para o programa é de fato **R$ 0,019 por ponto**.

### 3. Afirmação do Diretor: *"Nosso breakage está em 40%! Nossa meta é não passar de 20%!"*
* **Veredito:** ❌ **FALSA (Erro conceitual entre Breakage e Razão Expiração/Resgate).**
* **Evidências:**
  * O conceito contábil e de mercado de *Breakage* (IFRS 15) é a taxa de expiração sobre a emissão: $\frac{\text{Pontos Expirados}}{\text{Pontos Emitidos}}$.
  * Na migração de saldos legados (`op 100` e `103`):
    * Pontos migrados: 324.024.198
    * Pontos expirados da migração: 64.090.805
    * **Breakage Real da Migração = 19,78%** $\rightarrow$ **ESTÁ DENTRO DA META ($\le 20\%$)!**
  * Sobre o total emitido pelo programa (orgânico + migração): **8,38%**.
  * **De onde o Diretor tirou 40%?** No trimestre imediatamente anterior ao Pix (Fev-Abr/2026), a razão mensal entre **Expiração e Resgates** ($\frac{\text{Pontos Expirados}}{\text{Pontos Resgatados}}$) foi de 43,8% (Fev), 37,7% (Mar) e 36,2% (Abr), com **média de 38,95% (~40%)**. O diretor comparou *Expiração com Resgates*, e não com a emissão.

---

## 📊 Diagnóstico das Metas Contratuais e Saúde do Programa

| Mês | Aéreas % (Meta $\ge 50\%$) | Varejo % (Meta $\ge 20\%$) | Pix / Cashback % | Status do Contrato com Banco Aurora |
| :---: | :---: | :---: | :---: | :---: |
| **2026-04** | 80,7% | 19,3% | 0,0% | Aéreas OK, Varejo no limiar |
| **2026-05** | 74,8% | 20,3% | 4,9% | **Ambas Metas Cumpridas** |
| **2026-06** | 56,3% | **13,3%** | 30,4% | ⚠️ **Varejo Não Bateu** |
| **2026-07** | 57,9% | **12,8%** | 29,3% | ⚠️ **Varejo Não Bateu** |
| **2026-08** | 58,0% | **12,1%** | 29,9% | ⚠️ **Varejo Não Bateu** |
| **2026-09** | 59,0% | **13,0%** | 28,0% | ⚠️ **Varejo Não Bateu** |

### Conclusões de Negócio:
1. **O Pix não canibalizou Aéreas nem Varejo em termos absolutos:** Aéreas subiu de 15,2M pts (Abr/26) para 19,7M pts (Set/26), e o Varejo ficou estável em ~4,0M a 4,3M pts.
2. **O descumprimento da meta de Varejo decorre de diluição matemática:** O Pix adicionou entre 9M e 11M de pontos novos por mês no denominador total (elevando o total de resgates de ~19M para mais de ~33M pts).
3. **Saúde Financeira:** O Pix gera uma saída de caixa de **~R$ 175.000,00 por mês** em dinheiro líquido sem margem de produto para o grupo, ativando saldos dormentes de clientes das categorias **Essencial e Gold**.

---

## 💡 Recomendação para a Diretoria (Resumo)

Consulte o documento executivo completo em [`reports/apresentacao_diretoria.md`](file:///Users/luccasoliveira/.gemini/antigravity/scratch/case-ae-luccas/reports/apresentacao_diretoria.md).

1. **Renegociar a Meta de Varejo:** Propor aditivo com o Banco Aurora para expurgar o Pix do denominador do cálculo de Varejo (sob essa ótica, o Varejo representa 20,1% das trocas de catálogo, cumprindo a meta).
2. **Calibrar a Cotação do Pix:** Ajustar a conversão para R$ 0,017 por ponto (~59 pontos por R$ 1) ou introduzir taxa de serviço, gerando economia mensal de ~R$ 18.500 no caixa.
3. **Incentivo ao Varejo Próprio:** Criar benefício de conversão no app: pontos valendo R$ 0,022 em compras nos parceiros do grupo (Casa&Cia, MegaMagazine) vs. R$ 0,017 no Pix.
4. **Auditoria de Sistemas:** Corrigir com urgência a anomalia das 1.805 contas que sofreram débito de expiração de migração sem lastro de crédito.

---

## ❓ Hipóteses Assumidas e Perguntas aos Donos dos Sistemas/Negócio

### O que foi confirmado nos dados:
* Integridade dos 9 arquivos validada contra o manifesto SHA-256.
* Relação exata de R$ 0,019 por ponto em 100% dos resgates Pix aprovados.
* Reconciliação completa entre pedidos brutos e o relatório do operador.
* Cálculo formal de breakage da migração em 19,78%.

### Hipóteses Assumidas:
1. Assumiu-se que o contrato original de metas considerava apenas trocas por catálogo (Aéreas e Varejo), uma vez que o Pix inexistia na assinatura do contrato.
2. Assumiu-se que a coluna `control_group` do CRM deveria indicar o grupo de controle experimental, e por estar 100% nula, não houve medição de incrementalidade.

### Perguntas para os Responsáveis pelos Sistemas / Negócio:
1. **Engenharia de Sistemas:** Por que existem 1.805 contas em `points_ledger` com débitos de `EXPIRACAO_MIGRACAO` (operação 103) totalizando 10,18M pontos sem nenhum registro prévio de `CREDITO_MIGRACAO` (operação 100), fazendo com que essas contas fiquem com saldo negativo?
2. **Operações / Financeiro:** Qual o valor contratual exato que o Banco Aurora repassa à operadora por ponto emitido e por ponto expirado?
3. **Jurídico / Negócios:** Há previsão de penalidade financeira ou rescisão contratual no contrato com o banco pelo não atingimento da meta de 20% de Varejo nos meses de Junho a Setembro/2026?

---

## 🤖 Registro do Uso de IA

O uso de Inteligência Artificial neste case foi documentado de forma transparente e contínua em [`AI_LOG.md`](file:///Users/luccasoliveira/.gemini/antigravity/scratch/case-ae-luccas/AI_LOG.md).
* **Como a IA foi utilizada:**
  * Exploração e profiling automatizado dos 9 arquivos CSV com DuckDB.
  * Estruturação dos modelos de dados em camadas (Staging e Marts) e geração de testes em Pytest.
  * Formulação de testes de estresse adversariais para desafiar as conclusões preliminares.
* **O que foi conferido e corrigido:**
  * Reconciliação minuciosa dos pontos cancelados para comprovar o erro do operador.
  * Validação das fórmulas de breakage segundo a norma IFRS 15 vs. a métrica distorcida usada pelo diretor.
  * Investigação temporal das campanhas de Push para certificar que a rejeição da tese de CRM não possuía pontos cegos.
