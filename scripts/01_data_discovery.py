import hashlib
import json
import os
import duckdb
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "dados")
MANIFESTO_PATH = os.path.join(BASE_DIR, "MANIFESTO_v1.csv")

def verify_manifest():
    print("=== 1. VERIFICANDO MANIFESTO SHA-256 ===")
    manifest = pd.read_csv(MANIFESTO_PATH)
    all_ok = True
    for _, row in manifest.iterrows():
        filepath = os.path.join(DATA_DIR, row["arquivo"])
        if not os.path.exists(filepath):
            print(f"❌ {row['arquivo']}: Arquivo não encontrado!")
            all_ok = False
            continue
        with open(filepath, "rb") as f:
            computed_sha = hashlib.sha256(f.read()).hexdigest()
        if computed_sha == row["sha256"]:
            print(f"✅ {row['arquivo']}: SHA-256 OK ({row['linhas']} linhas)")
        else:
            print(f"❌ {row['arquivo']}: Divergência de hash!")
            print(f"   Esperado: {row['sha256']}")
            print(f"   Obtido:   {computed_sha}")
            all_ok = False
    return all_ok

def profile_tables():
    print("\n=== 2. PROFILING COM DUCKDB ===")
    con = duckdb.connect(database=":memory:")
    
    files = [
        "cards.csv",
        "carts.csv",
        "crm_events.csv",
        "dim_operation.csv",
        "order_items.csv",
        "orders.csv",
        "points_ledger.csv",
        "redeemed_points.csv",
        "relatorio_mensal_cliente.csv"
    ]
    
    summary = {}
    for f in files:
        tbl_name = f.replace(".csv", "")
        filepath = os.path.join(DATA_DIR, f)
        con.execute(f"CREATE TABLE {tbl_name} AS SELECT * FROM read_csv_auto('{filepath}')")
        
        row_count = con.execute(f"SELECT COUNT(*) FROM {tbl_name}").fetchone()[0]
        schema = con.execute(f"DESCRIBE {tbl_name}").fetchdf()
        
        print(f"\n--- Tabela: {tbl_name} ({row_count} linhas) ---")
        print(schema[["column_name", "column_type"]])
        
        # Amostra de 3 linhas
        sample = con.execute(f"SELECT * FROM {tbl_name} LIMIT 3").fetchdf()
        print("\nAmostra:")
        print(sample.to_string(index=False))
        
        summary[tbl_name] = {
            "row_count": row_count,
            "columns": schema["column_name"].tolist(),
            "types": schema["column_type"].tolist()
        }
        
    return con

if __name__ == "__main__":
    verify_manifest()
    con = profile_tables()
