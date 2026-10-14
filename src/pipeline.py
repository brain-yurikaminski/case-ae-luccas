"""
Pipeline de Analytics Engineering - Caso Pontua+
Executa todas as transformações de staging e marts no DuckDB e exporta tabelas para visualização e testes.
"""

import os
import duckdb
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
MODELS_DIR = os.path.join(BASE_DIR, "models")
STAGING_DIR = os.path.join(MODELS_DIR, "staging")
MARTS_DIR = os.path.join(MODELS_DIR, "marts")

def run_pipeline(db_path=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if db_path is None:
        db_path = os.path.join(OUTPUT_DIR, "pontua_plus.duckdb")
        # Remove versão anterior se existir para garantir idempotência
        if os.path.exists(db_path):
            os.remove(db_path)
            
    con = duckdb.connect(database=db_path)
    # Configura diretório de trabalho relativo para que read_csv_auto ache dados/
    con.execute(f"SET FILE_SEARCH_PATH='{BASE_DIR}'")
    
    print("=" * 60)
    print("🚀 EXECUTANDO PIPELINE DE ANALYTICS ENGINEERING (DUCKDB)")
    print("=" * 60)
    
    # 1. Camada Staging
    staging_models = [
        "stg_orders",
        "stg_order_items",
        "stg_carts",
        "stg_cards",
        "stg_points_ledger",
        "stg_crm_events",
        "stg_relatorio_mensal"
    ]
    
    print("\n📦 Construindo Camada Staging...")
    for model in staging_models:
        sql_file = os.path.join(STAGING_DIR, f"{model}.sql")
        with open(sql_file, "r") as f:
            query = f.read()
        con.execute(f"CREATE TABLE {model} AS {query}")
        count = con.execute(f"SELECT COUNT(*) FROM {model}").fetchone()[0]
        print(f"  ✅ {model}: {count:,} linhas")
        
    # 2. Camada Marts
    marts_models = [
        "fct_order_items",
        "fct_monthly_redemptions",
        "fct_pix_reconciliation",
        "fct_crm_attribution",
        "fct_breakage_analysis"
    ]
    
    print("\n🏛️ Construindo Camada Marts...")
    for model in marts_models:
        sql_file = os.path.join(MARTS_DIR, f"{model}.sql")
        with open(sql_file, "r") as f:
            query = f.read()
        con.execute(f"CREATE TABLE {model} AS {query}")
        count = con.execute(f"SELECT COUNT(*) FROM {model}").fetchone()[0]
        print(f"  ✅ {model}: {count:,} linhas")
        
        # Exporta CSV para visualização em output/
        csv_out = os.path.join(OUTPUT_DIR, f"{model}.csv")
        con.execute(f"COPY {model} TO '{csv_out}' (HEADER, DELIMITER ',')")
        
    print("\n✨ Pipeline executado com sucesso! Dados exportados para 'output/'.")
    return con

def print_executive_summary(con):
    print("\n" + "=" * 60)
    print("📊 RESUMO EXECUTIVO DAS METAS E AFIRMAÇÕES")
    print("=" * 60)
    
    print("\n1. Evolução Mensal dos Resgates e Metas Contratuais:")
    df_monthly = con.execute("""
        SELECT mes, pct_aereas, meta_aereas_atingida, pct_varejo, meta_varejo_atingida, pct_pix, pontos_totais
        FROM fct_monthly_redemptions
    """).fetchdf()
    print(df_monthly.to_string(index=False))
    
    print("\n2. Reconciliação do Pix (Desmascarando R$ 0,016 do Operador):")
    df_reconcile = con.execute("""
        SELECT mes, relatorio_razao_operador, custo_real_por_ponto_aprovado, 
               pontos_aprovados, pontos_brutos_sistema, transacoes_batem_com_bruto
        FROM fct_pix_reconciliation
    """).fetchdf()
    print(df_reconcile.to_string(index=False))
    
    print("\n3. Atribuição de CRM do Pix (Avaliando Afirmação de Sucesso da Comunicação):")
    df_crm = con.execute("""
        SELECT 
            canal_atribuicao, 
            count(*) as usuarios,
            round(count(*) * 100.0 / sum(count(*)) over(), 2) as pct
        FROM fct_crm_attribution
        GROUP BY 1
        ORDER BY 2 DESC
    """).fetchdf()
    print(df_crm.to_string(index=False))
    
    print("\n4. Análise de Breakage (Avaliando Afirmação do Diretor de 40% vs Meta 20%):")
    df_breakage = con.execute("""
        SELECT escopo_analise, taxa_percentual, meta_teto_pct, status_avaliacao
        FROM fct_breakage_analysis
    """).fetchdf()
    print(df_breakage.to_string(index=False))

if __name__ == "__main__":
    con = run_pipeline()
    print_executive_summary(con)
