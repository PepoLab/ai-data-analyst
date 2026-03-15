from langchain_community.llms import Ollama
from agent.tools import sql_tool
from agent.prompts import SYSTEM_PROMPT_SQL, SYSTEM_PROMPT_ANALYSIS
from agent.sql_validator import validate_sql
from agent.sql_cleaner import clean_sql
from database.schema_reader import get_schema


# inicializa modelo local
llm = Ollama(model="llama3")


def ask_agent(question):

    # -----------------------------
    # OBTER SCHEMA DO BANCO
    # -----------------------------
    schema = get_schema()

    # -----------------------------
    # GERAR SQL
    # -----------------------------
    prompt_sql = f"""
{SYSTEM_PROMPT_SQL}

Schema do banco:

{schema}

Pergunta do usuário:
{question}
"""

    sql = llm.invoke(prompt_sql)

    print("\nSQL gerado pelo modelo:")
    print(sql)

    # -----------------------------
    # LIMPAR SQL
    # -----------------------------
    sql = clean_sql(sql)

    print("\nSQL limpo:")
    print(sql)

    # -----------------------------
    # VALIDAR SQL
    # -----------------------------
    validate_sql(sql)

    # -----------------------------
    # EXECUTAR QUERY
    # -----------------------------
    result = sql_tool(sql)

    # -----------------------------
    # ORDENAR RESULTADO
    # -----------------------------
    if hasattr(result, "columns") and len(result.columns) > 1:
        try:
            result = result.sort_values(by=result.columns[-1], ascending=False)
        except Exception as e:
            print("\nNão foi possível ordenar os resultados:", e)

    print("\nDados retornados:")
    print(result)

    # -----------------------------
    # GERAR ANÁLISE
    # -----------------------------
    print("\nGerando análise dos dados...")

    # limitar tamanho enviado ao modelo
    try:
        result_preview = result.head(20)
    except:
        result_preview = result

    # converter dataframe para texto
    result_text = result_preview.to_string(index=False)

    prompt_analysis = f"""
{SYSTEM_PROMPT_ANALYSIS}

Pergunta do usuário:
{question}

Tabela de resultados:

{result_text}

Analise os dados acima e produza insights.

Regras:
- identifique os maiores e menores valores
- destaque padrões relevantes
- explique o que os números indicam
- seja objetivo
- responda em português
- não mencione SQL
"""

    print("\nPrompt de análise enviado ao modelo:")
    print(prompt_analysis)

    # chamada ao modelo
    explanation = llm.invoke(prompt_analysis)

    print("\nResposta bruta do modelo:")
    print(explanation)

    return explanation,result