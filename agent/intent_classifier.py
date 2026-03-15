from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

PROMPT_INTENT = """
Classifique a pergunta do usuário em apenas uma categoria:

DATA_QUESTION → pergunta sobre dados ou métricas
EXPLANATION → explicação de conceito
GREETING → saudação ou conversa

Responda apenas com o nome da categoria.

Pergunta:
{question}
"""


def classify_intent(question):

    prompt = PROMPT_INTENT.format(question=question)

    response = llm.invoke(prompt)

    intent = response.strip()

    return intent