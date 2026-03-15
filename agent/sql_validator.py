import re

FORBIDDEN = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"
]

def validate_sql(query: str):

    query_upper = query.upper()

    for word in FORBIDDEN:
        if word in query_upper:
            raise ValueError(f"Comasndo proibido detectado: {word}")

    if not query_upper.strip().startswith("SELECT"):
        raise ValueError("Apenas queries SELECT são permitidas")

    return query    