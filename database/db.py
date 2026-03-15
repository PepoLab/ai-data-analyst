import sqlite3
import pandas as pd

DB_PATH = "vendas.db"


def create_database():
    
    # lê o csv
    df = pd.read_csv("data/vendas.csv")

    # abre conexão
    conn = sqlite3.connect(DB_PATH)

    # salva no banco
    df.to_sql(
        "vendas",
        conn,
        if_exists="replace",
        index=False
    )

    # fecha conexão
    conn.close()

    print("Banco criado com sucesso!")


def run_query(query):

    # abre conexão
    conn = sqlite3.connect(DB_PATH)

    # executa query
    df = pd.read_sql(query, conn)

    # fecha conexão
    conn.close()

    return df