from agent.agent import ask_agent

while True:

    question = input("\nPergunte algo sobre os dados: ")

    response = ask_agent(question)

    print("\nInsight:")
    print(response)