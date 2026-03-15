import sqlite3

def get_schema():

    conn = sqlite3.connect("vendas.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(vendas)")
    columns = cursor.fetchall()

    schema = "Tabela vendas:\n"

    for column in columns:
        schema += f"- {column[1]} ({column[2]})\n"

    return schema