---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #060A1C
color: #EAF0FF
style: |
  @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
  section {
    font-family: 'Inter', system-ui, sans-serif;
    padding: 44px;
    background-color: #060A1C;
    color: #EAF0FF;
  }
  h1, h2 {
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
    letter-spacing: -0.02em;
  }
  h1 { font-size: 2.1rem; color: #EAF0FF; }
  h2 { font-size: 1.65rem; color: #00CFFF; }
  h3 {
    font-family: 'Roboto Mono', monospace;
    color: #A9B4D0;
    font-size: 1.05rem;
    font-weight: 400;
  }
  table {
    font-size: 0.74rem;
    width: 100%;
    border-collapse: collapse;
    font-family: 'Roboto Mono', monospace;
    border: 1px solid rgba(255,255,255,0.09);
  }
  th {
    background-color: #0A0F28;
    color: #00CFFF;
    padding: 8px 10px;
    border-bottom: 2px solid #1E2BFF;
    text-transform: uppercase;
    font-size: 0.7rem;
  }
  td {
    padding: 7px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.09);
    color: #A9B4D0;
  }
  .badge-pass { color: #3DFF6E; font-weight: bold; }
  .badge-fail { color: #FF4D4F; font-weight: bold; }
  .badge-warn { color: #FAAD14; font-weight: bold; }
  .highlight-card {
    background: #0E142F;
    border-radius: 0px;
    padding: 16px 20px;
    margin: 12px 0;
    border: 1px solid rgba(255,255,255,0.09);
    border-left: 3px solid #00CFFF;
  }
  code {
    font-family: 'Roboto Mono', monospace;
    background: rgba(0,207,255,0.08);
    color: #00CFFF;
    padding: 2px 6px;
    border-radius: 0px;
  }
  footer {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.65rem;
    color: #6B7699;
  }
---

# Programa Pontua+ · Banco Aurora
## Diagnóstico do Pix, Auditoria das Afirmações e Recomendações Estratégicas

**Apresentador:** Lucas Oliveira (Analytics Engineering)  
**Data:** Outubro / 2026  
**Case:** Brain003 · Branch: `entrega`

---

## 📑 Sumário Executivo & Agenda da Apresentação

* **[Bloco 1] Modelo Econômico & Ruptura do Pix:** As 5 engrenagens de lucro e o impacto da queima em dinheiro vivo *(Slides 03 e 04)*.
* **[Bloco 2] Diagnóstico Transacional:** Salto de +70% no resgate e efeito de diluição matemática no Varejo *(Slide 05)*.
* **[Bloco 3] Auditoria Analítica das 3 Hipóteses:** Veredito sobre CRM (campanhas), Operador (custo) e Diretor (breakage) *(Slides 06 a 08)*.
* **[Bloco 4] Engenharia de Dados & Decisões Técnicas:** Arquitetura DuckDB, modelagem dimensional em camadas, grain e 12 testes no Pytest *(Slides 09 a 11)*.
* **[Bloco 5] Alertas Operacionais de Sistemas:** Fricção de 14,4% de falha no Pix e 1.805 contas negativas no ledger *(Slide 12)*.
* **[Bloco 6] Recomendações Estratégicas & Próximos Passos:** Plano em 4 pilares de viabilidade financeira e governança *(Slides 13 e 14)*.

---

## 🏛️ Prefácio: Como o Programa Realmente Ganha Dinheiro?
### *O Modelo de Negócio do Pontua+ em 5 Etapas*

1. **Venda de Pontos ao Banco [*earn*]:** O Banco Aurora recolhe a taxa de intercâmbio dos cartões e compra pontos do Pontua+ em dinheiro vivo.
2. **Dinheiro Rendendo no Banco [*float*]:** Entre a emissão e o resgate (12 a 24 meses), o saldo recebido do banco fica investido rendendo CDI.
3. **Pontos que Expiram [*breakage*]:** Os clientes esquecem ou deixam vencer pontos. O programa fica com **100% de margem de lucro**.
4. **Margem na Entrega de Produtos [*burn*]:**
   * **Varejo Próprio (Casa&Cia, MegaMagazine):** Compra no atacado e lucra 20% a 30% no spread comercial.
   * **Aéreas:** Produto de prestígio com margem apertada (chamariz de alta renda).
5. **Venda Direta de Pontos Extras [*top-up*]:** Venda de recarga de pontos no cartão.

---

## ⚠️ O Ponto de Ruptura: Por que o Pix Rompeu a Lógica?

Ao lançar o Pix a **R$ 0,019 por ponto** em 27/05/2026:

* 🚫 **Zera a Margem Comercial:** O programa entrega dinheiro líquido à vista (desembolso de ~R$ 175k/mês) sem capturar margem de produto.
* 📉 **Destrói o Lucro da Expiração (*Breakage*):** Clientes de entrada (**Essencial e Gold**), que antes deixavam saldos expirarem (gerando lucro de 100%), agora sacam o dinheiro no Pix.
* 💸 **Mais Caro que Passagem Aérea:** Pagar R$ 0,019 em dinheiro vivo custa mais do que bancar uma passagem aérea (~R$ 0,0162) ou um produto no varejo (~R$ 0,0125).
* ⚖️ **Fura a Meta do Contrato:** O volume massivo do Pix diluiu a fatia percentual do Varejo para ~13%, descumprindo a meta de 20%.

---

## 📈 Diagnóstico: O Que Aconteceu Após o Pix?
### *Volume de resgates saltou de ~18M para mais de ~33M pontos/mês (+70%)*

| Mês | Aéreas (pts) | Aéreas % (Meta $\ge 50\%$) | Varejo (pts) | Varejo % (Meta $\ge 20\%$) | Pix (pts) | Pix % | Total Pontos |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2026-04 (Pré-Pix)** | 15.212.500 | **80,7%** <span class="badge-pass">✅</span> | 3.630.976 | **19,3%** <span class="badge-warn">⚠️</span> | 0 | 0,0% | 18.843.476 |
| **2026-05 (Lançamento)** | 16.111.500 | **74,8%** <span class="badge-pass">✅</span> | 4.365.976 | **20,3%** <span class="badge-pass">✅</span> | 1.051.095 | 4,9% | 21.528.571 |
| **2026-06** | 17.091.900 | **56,3%** <span class="badge-pass">✅</span> | 4.044.484 | **13,3%** <span class="badge-fail">❌</span> | 9.215.135 | 30,4% | 30.351.519 |
| **2026-07** | 17.687.900 | **57,9%** <span class="badge-pass">✅</span> | 3.894.815 | **12,8%** <span class="badge-fail">❌</span> | 8.960.664 | 29,3% | 30.543.379 |
| **2026-08** | 18.180.800 | **58,0%** <span class="badge-pass">✅</span> | 3.804.035 | **12,1%** <span class="badge-fail">❌</span> | 9.366.874 | 29,9% | 31.351.709 |
| **2026-09** | 19.762.300 | **59,0%** <span class="badge-pass">✅</span> | 4.336.420 | **13,0%** <span class="badge-fail">❌</span> | 9.385.666 | 28,0% | 33.484.386 |

* **Quem usou o Pix?** Principalmente cartões **Essencial e Gold** (2.027 pedidos; 48% dos pontos Pix). Cartões **Black e Infinite** continuam focados em Aéreas.

---

## 🎯 Por que o Varejo Caiu Abaixo dos 20%?
### *Diluição de Denominador vs. Queda de Volume Real*

* 🔎 **O Varejo Não Encolheu:**
  * Volume em Abril/26 (pré-Pix): **3,63M pontos**.
  * Volume em Setembro/26 (pós-Pix): **4,34M pontos**.
  * O volume de resgate em Varejo permaneceu estável em torno de **~4M pontos/mês**.

* 💥 **O Efeito Diluição:**
  * O denominador total explodiu de **~19M para mais de ~33M pontos/mês** com a chegada do Pix (+10M pts/mês).
  * Como a fatia do Varejo permaneceu em ~4M, sua participação percentual foi matematicamente espremida de **~20% para ~13%**.

---

## 🔍 Afirmação 1 (CRM): "A comunicação explica o sucesso do Pix"
### ❌ **VEREDITO: FALSA / NÃO SE SUSTENTA NOS DADOS**

* **Anacronismo Temporal:** O Pix foi lançado em **27/05/2026**. O email de lançamento (`CMP_LANCAMENTO_PIX`) só saiu em **28/05 às 13:00**. Clientes já haviam resgatado Pix antes do envio.
* **Conversão Direta Ínfima:** Dos 2.140 clientes de Pix, **apenas 39 clientes (1,8%)** clicaram no email de lançamento.
* **Somando todos os canais (Email + Pushes da madrugada):** Apenas **63 clientes (2,9%)** converteram por clique em notificações.
* **Mais de 64,3% dos usuários resgataram de forma 100% orgânica** (descoberta no app e boca a boca).
* **Sem Grupo de Controle:** A coluna `control_group` é 100% nula no CRM; não houve teste A/B para aferir incrementalidade causal.

---

## 🔍 Afirmação 2 (Operador): "O Pix sai a R$ 0,016 por ponto"
### ❌ **VEREDITO: FALSA (Erro contábil grosseiro do operador)**

* **Auditoria no Transacional:** Em pedidos aprovados, **cada ponto foi liquidado a EXATAMENTE R$ 0,019000** em todos os meses.
* **De onde veio o R$ 0,016?** O operador dividiu os Reais pagos nos pedidos aprovados pelos Pontos brutos de **todos** os pedidos (incluindo cancelados, estornados e inválidos):
  $$\text{Junho/26}: \frac{\text{R\$ } 174.261,75 \text{ (Aprovados)}}{10.709.419 \text{ pts (Bruto com 118 pedidos cancelados)}} = \mathbf{R\$ } 0,016272$$
* **Impacto no Negócio:** O operador gerou uma ilusão de custo 15,8% menor, ocultando uma taxa de cancelamento de **14,4%** no Pix e um gasto de caixa **~R$ 30k/mês maior** do que o orçado.

---

## 🔍 Afirmação 3 (Diretor): "Nosso breakage está em 40%!"
### ❌ **VEREDITO: FALSA (Confusão conceitual entre Breakage e Burn Ratio)**

* **Conceito Contábil Real (IFRS 15):** $\text{Breakage} = \frac{\text{Pontos Expirados}}{\text{Pontos Emitidos}}$.
  * Na base migrada: $\frac{64.090.805 \text{ pts expirados}}{324.024.198 \text{ pts migrados}} = \mathbf{19,78\%}$.
  * **Está DENTRO da meta contratual de $\le 20\%$!**
  * Sobre a base total emitida (orgânica + migrada): **8,38%**.
* **De onde veio o 40% do Diretor?** No trimestre anterior ao Pix (Fev-Abr/2026), a razão $\frac{\text{Expiração}}{\text{Resgate}}$ foi de 43,8% (Fev), 37,7% (Mar) e 36,2% (Abr) $\rightarrow$ **Média de ~39%**.
* O diretor olhou para a relação de curto prazo entre *vencimento e resgate*, e não para o estoque emitido.

---

## 🛠️ Decisão Técnica 1: Arquitetura DuckDB + Camadas dbt-like
### *Por que DuckDB e SQL modular em vez de scripts soltos de Pandas?*

* ⚡ **Engine OLAP In-Process (DuckDB):** Vetorizado, colunar e ultra-rápido. Executa ANSI SQL puro sobre os CSVs em milissegundos sem necessidade de configurar infraestrutura pesada de cluster.
* 📦 **Camada Staging (`models/staging/*.sql` - 7 views):**
  * Tipagem estrita (`TIMESTAMP`, `DOUBLE`, `VARCHAR`), saneamento de nulos e deduplicação de cartões.
  * Se a estrutura bruta mudar, apenas o staging é ajustado.
* 🏛️ **Camada Marts (`models/marts/*.sql` - 5 fatos):**
  * Modela as regras de negócio puras (reconciliação contábil, atribuição de CRM e breakage contábil).
* 🔁 **Idempotência:** O pipeline `src/pipeline.py` pode ser executado $N$ vezes produzindo exatamente o mesmo estado determinístico.

---

## 📐 Decisão Técnica 2: Modelagem Dimensional & Grain
### *Engenharia Reversa de Chaves e Contratos de Granularidade*

* 🔍 **A Descoberta da Chave Oculta:**
  * A tabela `orders` **não tinha** a coluna `user_id`.
  * Deduzimos e modelamos o join via `carts`:
    $$\text{orders} \xrightarrow{\text{cart\_id}} \text{carts} \xrightarrow{\text{user\_id}} \text{cards / crm\_events}$$
* 🎯 **Declaração Estrita de Grain para Evitar Fan-Out:**
  * `fct_order_items`: 1 linha por item de pedido (`order_item_id`).
  * `fct_monthly_redemptions`: 1 linha por mês e categoria (`ano_mes, categoria`).
  * `fct_pix_reconciliation`: 1 linha por mês de Pix (`ano_mes`).
  * `fct_crm_attribution`: 1 linha por cliente único de Pix (`user_id`).
  * `fct_breakage_analysis`: 1 linha por método contábil avaliado.

---

## 🧪 Decisão Técnica 3: Confiabilidade & 12 Testes no Pytest
### *Blindagem matemática contra alucinações e erros de reconciliação*

* 🔑 **Integridade Estrutural:** Unicidade de PKs e não-nulidade em campos monetários e temporais.
* 💰 **Invariâncias Contábeis:**
  * $\text{Aprovados} + \text{Cancelados} = \text{Bruto Total}$ validado centavo a centavo.
  * Custo real do Pix comprovado em **R$ 0,019000** com tolerância numérica de $10^{-5}$.
* 📋 **Validação de Regras Contratuais:** Asserções de que as metas de Aéreas ($\ge 50\%$) e Varejo ($\ge 20\%$) respondem dinamicamente às regras.
* ⏱️ **Execução Instantânea:** 12/12 testes executados em **0.20s** (`pytest tests/test_models.py`).

---

## 🚨 Alerta Operacional: Anomalias de Sistema Descobertas

<div class="highlight-card">

### 1. Fricção no Pix (14,4% de Falha em Junho/2026)
118 de 822 transações foram canceladas, estornadas ou invalidadas. Em transação bancária Pix, quase 15% de insucesso aponta para problemas de titularidade (CPF divergente), bloqueios excessivos de antifraude ou quedas de gateway.
</div>

<div class="highlight-card">

### 2. Anomalia Cadastral no Ledger de Pontos
**1.805 contas** sofreram débito de `EXPIRACAO_MIGRACAO` (op 103) totalizando **10,18M pontos** sem nunca terem recebido o `CREDITO_MIGRACAO` (op 100), fazendo com que essas contas ficassem com **saldo negativo** no sistema.
</div>

---

## 💡 Recomendação Estratégica: O Que Fazer com o Pix?
### 🎯 *NÃO COIBIR ABRUPTAMENTE, MAS REEQUILIBRAR A OPERAÇÃO*

1. **Repactuação da Meta com o Banco Aurora:** Propor *carve-out* do Pix no cálculo do catálogo. Se expurgarmos o Pix, o Varejo atinge **20,1%** das trocas de catálogo, cumprindo a meta.
2. **Reprecificação do Ponto Pix:** Reajustar a taxa para **R$ 0,013 - R$ 0,014 por ponto** (~75 pts/R$ 1). Estanca o subsídio e economiza **~R$ 60 mil/mês** no caixa.
3. **Smart Nudge para o Varejo Próprio:** Na tela do Pix, oferecer R$ 0,022/pt em vouchers da Casa&Cia e MegaMagazine vs. R$ 0,014 no Pix. O cliente ganha 40% a mais de poder de compra e o dinheiro fica no grupo.
4. **Saneamento do Ledger:** Auditar e regularizar as 1.805 contas com saldo negativo.

---

## ❓ O Que Ainda Falta Saber? (Perguntas aos Stakeholders)

* **Com o Banco Aurora / Jurídico:**
  * Qual a penalidade formal estipulada caso o banco não aceite expurgar o Pix da meta de Varejo?
  * Qual é o valor contratual exato que o banco repassa à operadora por ponto emitido e expirado?
* **Com os Parceiros de Varejo (Casa&Cia / MegaMagazine):**
  * Qual a margem comercial de contribuição média que o grupo captura em cada resgate de produto?
* **Com a Engenharia de Sistemas:**
  * O que causou o débito de expiração em 1.805 contas sem o crédito original de migração?
  * Quais os motivos técnicos dos 14,4% de cancelamentos em resgates Pix?

---

# Obrigado!
## Perguntas e Discussão

Lucas Oliveira · Analytics Engineering  
Brain003 · Case Pontua+ · Outubro/2026
