# 📘 Guia de Estudo e Roteiro de Apresentação · Case Analytics Engineer Brain003
**Candidato:** Lucas Oliveira  
**Tempo Total de Reunião:** 45 minutos (Divisão planejada: **~20 min de apresentação** + **15 a 20 min de sabatina/dúvidas**)  
**Repositório:** `https://github.com/brain-yurikaminski/case-ae-luccas/tree/entrega`  
**Objetivo deste Documento:** Permitir que você estude e revise em qualquer dispositivo (celular, tablet ou outro computador) toda a lógica de negócios, as provas matemáticas, as decisões arquiteturais de engenharia de dados e as respostas prontas para a banca.

---

# 🏛️ PARTE 1: Como o Negócio Realmente Funciona (Economia de Programas de Pontos)

Para impressionar a diretoria e a banca técnica, você precisa demonstrar que **não é apenas um operador de SQL**, mas alguém que compreende a dinâmica financeira do balanço da empresa.

### As 5 Engrenagens Financeiras do Pontua+

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 COMO O PROGRAMA PONTUA+ REALMENTE LUCRA                     │
├───────────────────┬───────────────────────────────┬─────────────────────────┤
│ 1. EARN (Venda)   │ 2. FLOAT (Rendimento CDI)     │ 3. BREAKAGE (Expiração) │
│ • Banco Aurora    │ • O cliente demora de 12 a    │ • Pontos que vencem sem │
│   paga em dinheiro│   24 meses para juntar pontos │   resgate viram 100% de │
│   ao Pontua+ a cada│ • O dinheiro adiantado pelo  │   margem de lucro líqui-│
│   ponto emitido   │   banco rende CDI no caixa    │   da para o programa    │
├───────────────────┴───────────────────────────────┴─────────────────────────┤
│ 4. BURN MARGIN (Margem no Resgate de Produtos)                              │
│ • Varejo Próprio (Casa&Cia, MegaMagazine): Compra no atacado de fábrica com │
│   desconto e captura de 20% a 30% de margem comercial na troca.             │
│ • Aéreas: Margem apertada, mas serve de chamariz para cartões Black/Infinite.│
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. TOP-UP (Venda Direta de Pontos Extras)                                   │
│ • Venda com cartão de crédito de pontos faltantes (R$ 101k faturados no período)│
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Venda de Pontos ao Banco [*Earn*]:**
   * O cliente passa o cartão de crédito do Banco Aurora. O banco cobra a taxa de intercâmbio (*interchange fee*) do lojista (ex: 1,5% a 2,0%).
   * Com esse dinheiro, o banco **compra pontos em moeda corrente líquida** do Pontua+. Ou seja, o dinheiro entra no caixa do Pontua+ **muito antes** do cliente sequer pensar em resgatar.
2. **Dinheiro Rendendo no Caixa [*Float*]:**
   * O cliente demora entre 12 a 24 meses para acumular saldo suficiente para uma passagem aérea ou televisão.
   * Durante todo esse tempo, o dinheiro adiantado pelo banco fica investido no tesouro/CDI gerando receita financeira passiva para o programa.
3. **Pontos que Expiram [*Breakage*]:**
   * Uma parcela dos clientes esquece os pontos ou deixa o prazo de validade expirar.
   * Como o banco já pagou por esses pontos no passado e a empresa não precisará entregar nenhum produto ou dinheiro por eles, **os pontos expirados viram 100% de margem de lucro líquido contábil**.
4. **Margem Comercial no Resgate de Mercadorias [*Burn*]:**
   * **Varejo Próprio (Casa&Cia e MegaMagazine):** O grupo compra produtos direto da indústria a preço de atacado. Quando o cliente troca 50.000 pontos por uma geladeira, o custo contábil do produto para o grupo é de R$ 0,0125/pt, mas o valor de mercado percebido é R$ 0,017/pt. O grupo lucra **20% a 30% no spread comercial**.
   * **Passagens Aéreas:** Produto caro e com margem comercial estreita (custo de ~R$ 0,0162/pt). Funciona como produto de prestígio para fidelizar clientes de alta renda (Black e Infinite) que geram alto volume de compras no cartão.
5. **Venda Direta de Pontos Extras [*Top-up*]:**
   * Clientes pagam com cartão de crédito para completar pequenos saldos faltantes para fechar um pacote turístico.

---

### ⚠️ Por que o "Pontos no Pix" Rompeu Essa Lógica Econômica?

Em **27/05/2026**, o programa lançou o resgate via Pix à taxa fixa de **R$ 0,019 por ponto** (ou ~52 pontos por R$ 1,00). Isso atacou diretamente os pilares de rentabilidade:

1. **Zera a Margem Comercial de Produto:** No Pix não há produto de atacado para capturar desconto. O programa precisa **desembolsar dinheiro vivo líquido da conta bancária (~R$ 175.000/mês)**.
2. **Destrói o Lucro de Expiração (*Breakage*):** Clientes com cartões de entrada (**Essencial e Gold**), que antes acumulavam 1.000 ou 2.000 pontos e deixavam expirar (gerando 100% de lucro para o programa), agora sacam R$ 20, R$ 40 ou R$ 50 no Pix antes de vencer.
3. **Custa mais caro do que Passagem Aérea:** Pagar R$ 0,019 em dinheiro líquido é economicamente pior do que pagar ~R$ 0,0162 em passagens aéreas ou ~R$ 0,0125 em mercadorias do varejo.
4. **Efeito Diluição na Meta Contratual do Varejo ($\ge 20\%$):**
   * Em Abril/26 (pré-Pix): Varejo representava **19,3%** das trocas (3,63M de pontos em um total de 18,8M).
   * Em Junho-Setembro/26 (pós-Pix): O volume de Varejo continuou estável em torno de **~4M de pontos/mês**.
   * Porém, a entrada de **+10 milhões de pontos/mês de Pix** inflou o denominador total de ~19M para mais de ~33M de pontos (+70%).
   * A fatia do Varejo foi espremida matematicamente para **~12% a 13%**, gerando um falso alerta de descumprimento contratual com o Banco Aurora.

---

# 🔍 PARTE 2: Veredito da Auditoria Analítica das 3 Afirmações

| Stakeholder | Afirmação Original | Veredito | Prova Matemática / Fato Incontestável |
| :--- | :--- | :---: | :--- |
| **CRM** | *"A comunicação de lançamento explica o sucesso do Pix"* | ❌ **FALSA** | • O Pix lançou em 27/05. O email só saiu em 28/05 às 13:00 (timing invertido).<br>• Dos 2.140 clientes de Pix, **apenas 39 clientes (1,8%)** clicaram no email.<br>• Somando push + email, apenas **2,9%** converteram via clique.<br>• **64,3% foram 100% orgânicos** (descoberta no app e boca a boca).<br>• Coluna `control_group` 100% nula (sem teste A/B para provar causalidade). |
| **Operador** | *"O custo do Pix sai a R$ 0,016 por ponto"* | ❌ **FALSA** | • Em 100% dos pedidos aprovados, o custo foi de **exatamente R$ 0,019000**.<br>• O operador dividiu os Reais aprovados pelos Pontos brutos de **todos** os pedidos (incluindo cancelados/estornados):<br>$$\text{Jun/26: } \frac{\text{R\$ } 174.261,75}{10.709.419 \text{ pts (bruto com 118 cancelados)}} = \mathbf{R\$ } 0,016272$$<br>• Escondeu da diretoria um rombo de caixa **~R$ 30k/mês maior** e uma taxa de cancelamento de **14,4%**. |
| **Diretor** | *"Nosso breakage está em 40%!"* | ❌ **FALSA**<br>*(Meta OK)* | • Pela norma contábil internacional (**IFRS 15**): $\text{Breakage} = \frac{\text{Expirados}}{\text{Emitidos}}$.<br>• Na base migrada: $\frac{64.090.805 \text{ pts}}{324.024.198 \text{ pts}} = \mathbf{19,78\%}$ (estritamente **dentro da meta de $\le 20\%$**).<br>• O diretor olhou para a relação de curto prazo entre $\frac{\text{Expiração}}{\text{Resgate}}$ no início de 2026 (Fev: 43,8%, Mar: 37,7%, Abr: 36,2% $\rightarrow$ média **~38,9%**). Confundiu queima mensal com taxa de perda sobre estoque. |

### Os Dois Alertas Críticos de Sistemas Descobertos:
1. **Fricção de 14,4% de cancelamento no Pix (Junho/2026):** 118 de 822 transações falharam ou foram invalidadas (CPF divergente da chave Pix, timeout de gateway e falso-positivo de antifraude).
2. **Anomalia Cadastral de Saldo Negativo (1.805 contas):** Sofreram débito de `EXPIRACAO_MIGRACAO` (op 103) somando 10,18M de pontos sem nunca terem recebido o `CREDITO_MIGRACAO` (op 100). Operam com saldo negativo no banco de dados.

---

# 🛠️ PARTE 3: Decisões Técnicas de Engenharia de Dados (O "Por que fizemos assim")

Esta é a parte que o seu entrevistador pediu expressamente no áudio. Use os argumentos abaixo para demonstrar senioridade técnica.

### Decisão 1: Arquitetura com DuckDB + SQL em Camadas (Staging & Marts)
* **Por que DuckDB?**
  * É um motor analítico colunar vetorizado in-process (o "SQLite para Analytics").
  * Permite rodar ANSI SQL de alta performance diretamente sobre arquivos CSV sem necessidade de subir um container Docker pesado ou pagar banco em nuvem para testar o case.
  * Execução local instantânea: processa ~400 mil linhas e roda 12 testes em menos de **1 segundo**.
* **Por que dividir em Camadas (`staging` e `marts`)?**
  * Segue o padrão da indústria (dbt / Medallion).
  * **Staging (7 views):** Limpeza técnica, tipagem (`TIMESTAMPTZ`, `DOUBLE`, `VARCHAR`), sanitização de strings e deduplicação de cartões (`stg_cards`). Se a estrutura do arquivo bruto mudar, apenas o staging é alterado.
  * **Marts (5 fatos):** Regras de negócio puras (reconciliação contábil, atribuição de marketing e cálculo de metas). Ficam 100% blindados de mudanças nas fontes brutas.
* **Idempotência do Pipeline (`src/pipeline.py`):**
  * O pipeline foi desenhado para ser determinístico: rodar 1 vez ou 1.000 vezes reconstrói a base sem gerar duplicações nem efeitos colaterais nos dados originais.

### Decisão 2: Engenharia Reversa de Chaves e Contratos de Grain (Granularidade)
* **O Desafio da Chave Oculta:**
  * No profiling inicial, descobrimos que a tabela `orders` **não tinha a coluna `user_id`** (era 100% nula). Sem ela, seria impossível cruzar os resgates com os eventos de CRM e perfil do cliente.
  * **A Solução:** Mapeamos dimensionalmente o relacionamento via `carts`:
    $$\text{orders.cart\_id} \xrightarrow{1:1} \text{carts.cart\_id} \xrightarrow{N:1} \text{carts.user\_id} \rightarrow \text{cards / crm\_events}$$
* **Grain Formalmente Declarado para Evitar Fan-Out:**
  * O maior erro de junções em SQL é o *fan-out* (multiplicação de valores por join N:N). Declaramos formalmente o grain de cada modelo:
    * `fct_order_items`: 1 linha por item de pedido (`order_item_id`).
    * `fct_monthly_redemptions`: 1 linha por mês e categoria (`ano_mes, categoria`).
    * `fct_pix_reconciliation`: 1 linha por mês de transação Pix (`ano_mes`).
    * `fct_crm_attribution`: 1 linha por cliente único de Pix (`user_id`).
    * `fct_breakage_analysis`: 1 linha por metodologia contábil avaliada.

### Decisão 3: Confiabilidade dos Dados & Pirâmide de 12 Testes no Pytest
* **Por que testes automatizados em código?**
  * Para eliminar o risco de erro humano ou alucinações de cálculos manuais.
  * Testamos:
    1. Unicidade de PKs em staging e marts.
    2. Não-nulidade em campos financeiros e timestamps.
    3. **Invariância contábil estrita:** $\text{Aprovados} + \text{Cancelados} = \text{Bruto Total}$ validado centavo a centavo.
    4. **Tolerância matemática de ponto flutuante ($10^{-5}$):** Comprovando que o custo aprovado é de exatamente R$ 0,019000.
    5. Atribuição de CRM: A soma de clientes únicos de Pix no fato de CRM é exatamente igual aos 2.140 clientes da tabela transacional.

### Trade-offs e Alternativas Descartadas (O que você ponderou e rejeitou)
* *Descartamos Pandas solto:* Porque lógica procedural em script Python dificulta auditoria SQL e não cria contratos de dados.
* *Descartamos Docker + PostgreSQL:* Porque adicionaria atrito de setup desnecessário para o avaliador (portas ocupadas, credenciais).
* *Descartamos Last-Touch ingênuo no CRM:* Porque atribuiria compras feitas em 27/05 a campanhas disparadas em 28/05. Exigimos restrição estrita de `event_timestamp <= order_timestamp`.

---

# 🤖 PARTE 4: A Dinâmica Humano + IA (A Cadeia de Raciocínio)

Se o entrevistador perguntar: *"Você usou IA? Como foi o processo?"*, aqui está a sua resposta de autoridade:

> *"Sim, utilizei IA como copiloto de execução e acelerador de digitação SQL — exatamente como se espera de um engenheiro moderno em 2026.*  
>  
> *No entanto, a IA foi estritamente o braço executor de sintaxe. Todo o direcionamento estratégico, a formulação das hipóteses adversariais, a checagem de premissas contábeis (IFRS 15) e a arquitetura em camadas foram decisões minhas como Engenheiro:*
> 1. *Quando a IA calculou o breakage inicialmente como Expiração / Resgate (~39%), eu rejeitei o resultado e impus a norma internacional IFRS 15 (Expirados / Emitidos), provando que o breakage era 19,78% e a meta estava cumprida.*
> 2. *Quando o operador alegou R$ 0,016, eu desconfiei do denominador, fiz a auditoria dos pedidos cancelados e provei que o custo real era R$ 0,019.*
> 3. *Fui eu quem descobriu a ausência de `user_id` em `orders` e orientou a engenharia reversa via `carts`.*
> 4. *E criei uma suíte com 12 testes no Pytest para auditar a própria IA e garantir que nenhum cálculo continha alucinações.*
> 
> *Tudo isso está documentado de forma transparente no arquivo `AI_LOG.md` no repositório."*

---

# ⏱️ PARTE 5: Roteiro Cronometrado de Apresentação (20 Minutos)

Abra o arquivo [apresentacao_diretoria_slides.html](file:///Users/luccasoliveira/.gemini/antigravity/scratch/case-ae-luccas/reports/apresentacao_diretoria_slides.html) no navegador em tela cheia (tecle `F`).

### [00:00 - 02:00] Abertura & Sumário Executivo (Slides 1 e 2)
* **Objetivo:** Mostrar clareza, segurança e domínio da agenda.
* **O que falar:**
  * *"Olá a todos. Trago hoje o diagnóstico do Programa Pontua+ após o lançamento do Pix em maio de 2026."*
  * *"Como vemos no Sumário (Slide 2), estruturei a apresentação em duas grandes frentes: primeiro, a visão de negócio, economia do programa e auditoria das 3 hipóteses; segundo, as decisões técnicas de engenharia de dados — arquitetura DuckDB, modelagem de grain e 12 testes no Pytest."*

### [02:00 - 05:00] Modelo Econômico & Ruptura do Pix (Slides 3 e 4)
* **Objetivo:** Explicar a economia do programa antes de entrar em números isolados.
* **O que falar:**
  * *"Para entender o Pix, precisamos ver como o Pontua+ ganha dinheiro: nas 5 engrenagens (venda de pontos adiantada ao banco, rendimento do float, lucro de 100% no breakage de pontos esquecidos, margem de 20-30% no varejo próprio e chamariz de aéreas)."*
  * *"O Pix rompeu essa lógica: entregou moeda corrente líquida sem margem de produto, canibalizou clientes que antes deixavam o saldo vencer e inflou o denominador total."*

### [05:00 - 09:00] Diagnóstico Transacional & Auditoria das 3 Hipóteses (Slides 5 a 8)
* **Objetivo:** Apresentar os vereditos analíticos com rigor matemático.
* **O que falar:**
  * **Slide 5:** *"O volume saltou +70%. O Varejo não caiu em volume absoluto (~4M pts/mês); o recuo para 13% é puramente diluição matemática do denominador pelo Pix."*
  * **Slide 6 (CRM):** *"Falsa. Lançamento em 27/05 e email em 28/05. Apenas 2,9% converteram por clique. 64,3% foram orgânicos e não houve grupo de controle."*
  * **Slide 7 (Operador):** *"Falsa. O custo real aprovado é de exatamente R$ 0,019. O operador dividiu Reais aprovados pelos pontos brutos de todos os pedidos incluindo cancelados, camuflando R$ 30k/mês de queima extra e 14,4% de falha no Pix."*
  * **Slide 8 (Diretor):** *"Falsa / Meta Cumprida. Pela norma contábil IFRS 15, o breakage é de 19,78%, dentro da meta de até 20%. O diretor olhou para a razão mensal expiração/resgates (média de 38,9% pré-Pix)."*

### [09:00 - 14:00] O Ponto Alto: Engenharia de Dados & Decisões Técnicas (Slides 9 a 11)
* **Objetivo:** Justificar a arquitetura técnica exatamente como o entrevistador pediu no áudio.
* **O que falar:**
  * **Slide 9 (Arquitetura):** *"Por que DuckDB e não scripts soltos de Pandas? DuckDB é colunar, vetorizado e executa ANSI SQL diretamente sobre os dados em milissegundos. Estruturei em camadas Staging (limpeza técnica e casts) e Marts (regras de negócio puras), com pipeline 100% idempotente."*
  * **Slide 10 (Modelagem & Grain):** *"No profiling, descobri que `orders` não tinha `user_id`. Mapeei a chave oculta via `carts` (`orders.cart_id -> carts.cart_id -> carts.user_id`). E declarei formalmente o grain de cada tabela fato para evitar fan-out de métricas."*
  * **Slide 11 (Pytest):** *"Para garantir zero alucinações, criei 12 testes automatizados. Eles garantem integridade de PKs, invariância de Reais e provam com tolerância de 10⁻⁵ que a conta do Pix fecha centavo a centavo."*

### [14:00 - 17:00] Alertas Operacionais de Sistemas & Riscos (Slide 12)
* **Objetivo:** Demonstrar visão sistêmica além da análise de dados.
* **O que falar:**
  * *"Identifiquei duas falhas graves de engenharia: 14,4% de falha nas transações Pix em junho (atrito no SAC e risco de gateway) e 1.805 contas operando com saldo negativo no ledger por débito indevido de migração sem crédito correspondente."*

### [17:00 - 20:00] Recomendações Estratégicas & Próximos Passos (Slides 13 e 14)
* **Objetivo:** Fechar com plano de ação executivo e abrir para a banca.
* **O que falar:**
  * *"Minha recomendação é não coibir o Pix, mas reequilibrá-lo em 4 pilares:  
    1. Repactuar a meta de Varejo com carve-out do Pix (expurgando o Pix, o Varejo atinge 20,1% e cumpre a meta);  
    2. Reprecificar o Pix para R$ 0,013 - R$ 0,014/ponto, economizando ~R$ 60 mil/mês no caixa;  
    3. Aplicar smart nudge bonificado na tela do app para vouchers do varejo próprio;  
    4. Sanear o ledger e exigir mesma titularidade (CPF) para o Pix.*  
  * *"Obrigado e estou à disposição para as perguntas da banca!"*

---

# 🎯 PARTE 6: Guia de Sobrevivência para a Sabatina (Perguntas da Banca)

### 1. "Por que você não usou dbt Core diretamente no projeto?"
> *"Porque dbt Core com banco externo exigiria que o avaliador instalasse dependências pesadas, configurasse um `profiles.yml` e subisse containers. O DuckDB nos permite aplicar os exatos mesmos princípios do dbt — modularidade, SQL puro desacoplado em pastas `staging` e `marts` e documentação de grão — mas rodando nativamente em um único script Python (`pipeline.py`). Se a Brain003 usa dbt em produção, a migração desses arquivos `.sql` é praticamente 1 para 1."*

### 2. "Como você garantiu que o join entre `crm_events` e `orders` não duplicou resgates?"
> *"Modelei a `fct_crm_attribution` com granularidade estrita de 1 linha por `user_id` de Pix, agrupando e ordenando pelo timestamp da primeira conversão direta antes de agregar. Além disso, criei um teste automatizado no Pytest (`test_crm_attribution_user_count`) que assegura que a contagem de clientes no fato de CRM é exatamente igual aos 2.140 clientes da tabela transacional."*

### 3. "E se esse pipeline fosse para Produção amanhã, o que mudaria?"
> *"A modelagem lógica e os SQLs permaneceriam os mesmos. O que mudaria seria a infraestrutura:  
> 1. Orquestração com Airflow ou Prefect rodando agendado diariamente;  
> 2. Os modelos rodando em cima de um Data Warehouse corporativo (BigQuery / Snowflake);  
> 3. CI/CD no GitHub Actions rodando a suíte de testes do Pytest em cada PR;  
> 4. Alertas no Slack caso a taxa de falha do Pix ultrapasse 5% em uma janela de 2 horas."*

### 4. "Por que você diz que o operador errou ao invés de dizer que o Pix é mais barato?"
> *"Porque a matemática contábil não mente. Em pedidos aprovados, o valor pago foi sempre de R$ 0,019000 por ponto. Para chegar a R$ 0,016, o operador dividiu os Reais aprovados pelos pontos brutos de pedidos cancelados, estornados e inválidos. Em contabilidade financeira, não se pode diluir o custo unitário de mercadorias entregues pelo volume de intenções de compras canceladas onde nenhum centavo saiu do caixa."*

### 5. "O Diretor não está certo em se preocupar com os 40% de expiração/resgate?"
> *"Ele tem razão em se preocupar com a velocidade de queima, mas usou o conceito e a métrica errados. A meta contratual com o Banco Aurora é de Breakage ($\le 20\%$). Breakage contábil (IFRS 15) mede a proporção de pontos emitidos que nunca serão resgatados (e que na migração deu 19,78%). O que deu ~39% foi a razão entre o que expirou e o que foi resgatado no trimestre Fev-Abr/26. Misturar essas duas métricas levaria a empresa a tomar decisões comerciais equivocadas achando que descumpriu o contrato."*

---

# 🏁 Checklist de Sucesso para a Reunião
- [ ] Conecte-se 5 minutos antes e teste áudio/vídeo.
- [ ] Deixe o arquivo `reports/apresentacao_diretoria_slides.html` aberto no navegador em aba cheia.
- [ ] Lembre-se: use as setas do teclado para avançar, ou clique no botão `📑 Sumário` / tecle `S` para voltar ao menu a qualquer momento.
- [ ] Mantenha postura serena e firme nos números: você descobriu as pegadinhas nos dados, construiu um pipeline com 12 testes e tem justificativa técnica para cada decisão.

**Você está com um dos melhores cases já produzidos para essa posição. Arrebenta lá! 🚀**
