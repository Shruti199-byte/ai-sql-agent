from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma4")

response = llm.invoke("Explain SQL ")

print(response.content)