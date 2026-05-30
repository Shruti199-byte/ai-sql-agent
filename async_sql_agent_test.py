import asyncio
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

DATABASE_URL = "postgresql+psycopg2://shruti:shruti123@localhost:5432/aisqldb"


async def run_question(agent, question):
    print("\nQuestion:", question)

    try:
        response = await agent.ainvoke({"input": question})
        print("Final Answer:", response["output"])
    except Exception as e:
        print("Failure/Error observed:")
        print(e)


async def main():
    db = SQLDatabase.from_uri(DATABASE_URL)

    llm = ChatOllama(
        model="gemma4",
        temperature=0
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        handle_parsing_errors=True
    )

    questions = [
        "List all students with their section names.",
        "Find the top 3 students based on average marks.",
        "Show students from section A who are also in the top 30 percent of the overall batch based on average marks.",
        "Show students whose attendance is below 75 percent."
    ]

    for question in questions:
        await run_question(agent, question)


if __name__ == "__main__":
    asyncio.run(main())