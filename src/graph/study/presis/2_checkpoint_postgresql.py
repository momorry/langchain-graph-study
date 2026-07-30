from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresCheckpointer
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph

from study.base.model.chat_model import get_model


class OverAllState(MessagesState):
    output: str


model = get_model()


def llm_node(state: OverAllState) -> OverAllState:
    ai_msg = model.invoke(state['messages'])
    return {"messages": ai_msg}


def output_node(state: OverAllState) -> OverAllState:
    return {"output": state["messages"][-1].content}



builder = StateGraph(state_schema=OverAllState)

builder.add_node(llm_node)
builder.add_node(output_node)
builder.add_edge(START, "llm_node")
builder.add_edge("llm_node", "output_node")
builder.add_edge("output_node", END)

# 定义并在编译时传递 Checkpointer
DB_URL = "postgresql://langgraph_user:123456@localhost:5432/langgraph_db?sslmode=disable"

with PostgresCheckpointer(DB_URL) as checkpointer:

    checkpointer.setup()
    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable":{"thread_id":"7498749875"}}

    graph.invoke({"messages": [HumanMessage("你好，我是老王")]},config = config)
    graph.invoke({"messages": [HumanMessage("从现在开始，你是小王")]},config = config)
    res = graph.invoke({"messages": [HumanMessage("我是谁，你是谁")]},config = config)

    print(res["output"])

    print("------------------------------------")
    for msg in res["messages"]:
        msg.pretty_print()