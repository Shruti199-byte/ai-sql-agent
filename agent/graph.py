from typing import Annotated, Literal
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from agent.tools import (
    ExecuteQueryTool,
    GetSchemaTool,
    ListTablesTool,
    ValidateQueryTool,
)

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


tools = [
    ListTablesTool(),
    GetSchemaTool(),
    ValidateQueryTool(),
    ExecuteQueryTool(),
]

llm = ChatOllama(model="gemma4", temperature=0)
llm_with_tools = llm.bind_tools(tools)


async def llm_node(state: AgentState) -> dict:
    print("\n[llm_node] Invoking LLM...")

    response = await llm_with_tools.ainvoke(state["messages"])

    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"[llm_node] → Tool call: '{tc['name']}' | Args: {tc['args']}")
    else:
        print("[llm_node] → LLM produced a final answer (no tool calls).")

    return {"messages": [response]}


tool_node = ToolNode(tools)


def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("[router] Routing to tool_node.")
        return "tools"

    print("[router] No tool calls — routing to END.")
    return END


graph_builder = StateGraph(AgentState)

graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tools", tool_node)

graph_builder.set_entry_point("llm")

graph_builder.add_conditional_edges(
    source="llm",
    path=should_continue,
    path_map={
        "tools": "tools",
        END: END,
    },
)

graph_builder.add_edge("tools", "llm")

app = graph_builder.compile()