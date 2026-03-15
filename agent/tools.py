from database.db import run_query

def sql_tool(query:str):

    result = run_query(query)

    return result