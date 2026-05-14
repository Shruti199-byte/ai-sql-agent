from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent


db = SQLDatabase.from_uri(
    "postgresql+psycopg2://shruti:shruti123@localhost:5432/aisqldb"
)


llm = ChatOllama(model="gemma4", temperature=0)


agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True
)


question = "Which employee has the highest salary?"

response = agent.invoke({"input": question})

print("\nFinal Answer:")
print(response["output"])