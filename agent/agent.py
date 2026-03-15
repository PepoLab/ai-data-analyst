from langchain_community.llms import Ollama

from agent.tools import sql_tool
from agent.prompts import SYSTEM_PROMPT_SQL, SYSTEM_PROMPT_ANALYSIS
from agent.sql_validator import validate_sql
from agent.sql_cleaner import clean_sql
from database.schema_reader import get_schema
from agent.intent_classifier import classify_intent


# -----------------------------
# INICIALIZA MODELO LOCAL
# -----------------------------
llm = Ollama(model="llama3")


# -----------------------------
# FUNÇÃO PRINCIPAL DO AGENTE
# -----------------------------
def ask_agent(question):

    # -----------------------------
    # CLASSIFICAR INTENÇÃO
    # -----------------------------
    intent = classify_intent(question)

    print("\nIntent detectada:", intent)

    # -----------------------------
    # GREETING
    # -----------------------------
    if intent == "GREETING":

        response = llm.invoke(f"""
Responda de forma amigável.

Pergunta:
{question}
""")

        return response, None

    # -----------------------------
    # EXPLICAÇÃO
    # -----------------------------
    if intent == "EXPLANATION":

        response = llm.invoke(f"""
Explique de forma clara e objetiva.

Pergunta:
{question}
""")

        return response, None

    # -----------------------------
    # PERGUNTA DE DADOS
    # -----------------------------
    if intent == "DATA_QUESTION":

        # -----------------------------
        # OBTER SCHEMA
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
                result = result.sort_values(
                    by=result.columns[-1],
                    ascending=False
                )
            except Exception as e:
                print("\nNão foi possível ordenar:", e)

        print("\nDados retornados:")
        print(result)

        # -----------------------------
        # GERAR ANÁLISE
        # -----------------------------
        print("\nGerando análise dos dados...")

        try:
            result_preview = result.head(20)
        except:
            result_preview = result

        result_text = result_preview.to_string(index=False)

        prompt_analysis = f"""
{SYSTEM_PROMPT_ANALYSIS}

Pergunta do usuário:
{question}

Tabela de resultados:

{result_text}

Analise os dados acima e produza insights.

Regras:
- identifique maiores e menores valores
- destaque padrões relevantes
- explique o que os números indicam
- seja objetivo
- responda em português
- não mencione SQL
"""

        print("\nPrompt enviado ao modelo:")
        print(prompt_analysis)

        explanation = llm.invoke(prompt_analysis)

        print("\nResposta do modelo:")
        print(explanation)

        return explanation, result

    # -----------------------------
    # FALLBACK
    # -----------------------------
    response = llm.invoke(f"""
Responda normalmente à pergunta abaixo:

{question}
""")

    return response, None