import re

def clean_sql(response):

    # remove markdown
    response = response.replace("```sql", "").replace("```", "")

    # encontra primeiro SELECT
    match = re.search(r"SELECT[\s\S]*?;", response, re.IGNORECASE)

    if match:
        sql = match.group(0)
    else:
        # fallback se não tiver ;
        match = re.search(r"SELECT[\s\S]*", response, re.IGNORECASE)
        sql = match.group(0) if match else response

    return sql.strip()