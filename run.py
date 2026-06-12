import asyncio
import pandas as pd
from langchain_core.messages import HumanMessage , ToolMessage

from agent.graph import app

def extract_last_dataframe(messages: list) -> pd.DataFrame | None:
    """Walk the message list in reverse and return the artifact from
    the last execute_query ToolMessage that has one."""
    for msg in reversed(messages):
        if (
            isinstance(msg, ToolMessage)
            and msg.name == "execute_query"
            and msg.artifact is not None
        ):
            return msg.artifact
    return None


async def ask(question):

    print(f"\nQuestion: {question}")

    result = await app.ainvoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )

    df = extract_last_dataframe(result["messages"]) 
    if df is not None:
         print("\nRows returned from database:")
         print(df.to_string())
         
    print("\nFinal Answer:")
    print(result["messages"][-1].content.strip())


async def main():

    questions = [
        "List all students with their section names.",
        #"Find the top 3 students based on average marks.",
        #"Show students from section A who are also in the top 30 percent of the overall batch based on average marks.",
        #"Show all marks."

    ]

    for question in questions:
        await ask(question)


if __name__ == "__main__":
    asyncio.run(main())