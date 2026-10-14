"""
Testes Automatizados de Qualidade, Unicidade e Reconciliação das Métricas
Executado via pytest.
"""

import os
import duckdb
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "output", "pontua_plus.duckdb")

@pytest.fixture(scope="session")
def con():
    if not os.path.exists(DB_PATH):
        from src.pipeline import run_pipeline
        run_pipeline(DB_PATH)
    connection = duckdb.connect(DB_PATH, read_only=True)
    yield connection
    connection.close()

# -------------------------------------------------------------------------
# 1. TESTES DE UNICIDADE (PRIMARY KEYS / GRAIN)
# -------------------------------------------------------------------------

def test_pk_uniqueness_stg_orders(con):
    res = con.execute("""
        SELECT order_id, COUNT(*) 
        FROM stg_orders 
        GROUP BY 1 
        HAVING COUNT(*) > 1
    """).fetchall()
    assert len(res) == 0, f"Chave duplicada encontrada em stg_orders: {res}"

def test_pk_uniqueness_stg_order_items(con):
    res = con.execute("""
        SELECT order_item_id, COUNT(*) 
        FROM stg_order_items 
        GROUP BY 1 
        HAVING COUNT(*) > 1
    """).fetchall()
    assert len(res) == 0, f"Chave duplicada em stg_order_items: {res}"

def test_pk_uniqueness_fct_order_items(con):
    res = con.execute("""
        SELECT order_item_id, COUNT(*) 
        FROM fct_order_items 
        GROUP BY 1 
        HAVING COUNT(*) > 1
    """).fetchall()
    assert len(res) == 0, f"Chave duplicada em fct_order_items: {res}"

def test_pk_uniqueness_fct_monthly_redemptions(con):
    res = con.execute("""
        SELECT mes, COUNT(*) 
        FROM fct_monthly_redemptions 
        GROUP BY 1 
        HAVING COUNT(*) > 1
    """).fetchall()
    assert len(res) == 0, f"Mês duplicado em fct_monthly_redemptions: {res}"

def test_pk_uniqueness_fct_crm_attribution(con):
    res = con.execute("""
        SELECT user_id, COUNT(*) 
        FROM fct_crm_attribution 
        GROUP BY 1 
        HAVING COUNT(*) > 1
    """).fetchall()
    assert len(res) == 0, f"Usuário duplicado em fct_crm_attribution: {res}"

# -------------------------------------------------------------------------
# 2. TESTES DE NÃO-NULIDADE EM CAMPOS CRÍTICOS
# -------------------------------------------------------------------------

def test_not_null_critical_fields_fct_order_items(con):
    null_counts = con.execute("""
        SELECT 
            COUNT(*) - COUNT(order_item_id) AS null_item_id,
            COUNT(*) - COUNT(order_id) AS null_order_id,
            COUNT(*) - COUNT(user_id) AS null_user_id,
            COUNT(*) - COUNT(mes) AS null_mes,
            COUNT(*) - COUNT(item_status) AS null_status
        FROM fct_order_items
    """).fetchone()
    assert null_counts == (0, 0, 0, 0, 0), f"Valores nulos encontrados em fct_order_items: {null_counts}"

# -------------------------------------------------------------------------
# 3. TESTES DE VALIDAÇÃO DAS 3 AFIRMAÇÕES DE NEGÓCIO
# -------------------------------------------------------------------------

def test_operador_pix_real_unit_cost_is_19_cents(con):
    """
    Garante que o custo por ponto de Pix em transações aprovadas
    é rigorosamente R$ 0,019 (desbancando o R$ 0,016 afirmado pelo operador).
    """
    res = con.execute("""
        SELECT 
            MIN(reais_por_ponto), 
            MAX(reais_por_ponto),
            ROUND(SUM(product_value) / SUM(paid_points), 3) AS media_ponderada
        FROM fct_order_items
        WHERE is_pix = TRUE AND is_approved = TRUE
    """).fetchone()
    min_rate, max_rate, avg_rate = res
    assert round(min_rate, 2) == 0.02
    assert round(max_rate, 2) == 0.02
    assert avg_rate == 0.019, f"Custo médio por ponto esperado 0.019, obtido: {avg_rate}"

def test_operador_pix_reconciliation_points_and_orders(con):
    """
    Comprova que o relatório do operador utilizou o denominador BRUTO
    (incluindo pedidos cancelados e estornados).
    """
    discrepancies = con.execute("""
        SELECT mes, relatorio_pontos, pontos_brutos_sistema, transacoes_batem_com_bruto, pontos_batem_com_bruto
        FROM fct_pix_reconciliation
        WHERE pontos_batem_com_bruto = FALSE OR transacoes_batem_com_bruto = FALSE
    """).fetchall()
    assert len(discrepancies) == 0, f"Discrepâncias na reconciliação do operador: {discrepancies}"

def test_diretor_breakage_within_target(con):
    """
    Garante que o breakage oficial da migração é de 19,78%, abaixo da meta de 20%.
    """
    breakage = con.execute("""
        SELECT taxa_percentual, meta_teto_pct, status_avaliacao
        FROM fct_breakage_analysis
        WHERE escopo_analise LIKE '%Migração%'
    """).fetchone()
    taxa, meta, status = breakage
    assert taxa == 19.78, f"Taxa de breakage esperada 19.78, obtida: {taxa}"
    assert taxa <= meta, f"Breakage {taxa}% ultrapassou a meta de {meta}%!"
    assert status == 'DENTRO DA META'

def test_crm_communication_does_not_explain_success(con):
    """
    Garante que menos de 5% dos usuários que resgataram Pix converteram
    via clique na comunicação, invalidando a afirmação do time de CRM.
    """
    click_pct = con.execute("""
        SELECT ROUND(COUNT(CASE WHEN canal_atribuicao = 'Direct Click Attribution' THEN 1 END) * 100.0 / COUNT(*), 2)
        FROM fct_crm_attribution
    """).fetchone()[0]
    assert click_pct < 5.0, f"Percentual de conversão por clique maior do que o esperado: {click_pct}%"

# -------------------------------------------------------------------------
# 4. TESTES DE METAS CONTRATUAIS
# -------------------------------------------------------------------------

def test_aereas_target_always_met(con):
    """
    Garante que a meta de Aéreas (>= 50%) foi cumprida em todos os meses.
    """
    failed_months = con.execute("""
        SELECT mes, pct_aereas 
        FROM fct_monthly_redemptions 
        WHERE meta_aereas_atingida = FALSE
    """).fetchall()
    assert len(failed_months) == 0, f"Meses em que Aéreas não bateu a meta de 50%: {failed_months}"

def test_varejo_target_breached_post_pix(con):
    """
    Garante que a meta de Varejo (>= 20%) foi descumprida após a entrada plena do Pix (Junho a Setembro).
    """
    failed_post_pix = con.execute("""
        SELECT mes, pct_varejo 
        FROM fct_monthly_redemptions 
        WHERE mes >= '2026-06' AND meta_varejo_atingida = TRUE
    """).fetchall()
    assert len(failed_post_pix) == 0, f"Varejo deveria ter ficado abaixo de 20% pós-Pix: {failed_post_pix}"
