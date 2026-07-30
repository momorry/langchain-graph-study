from idlelib import config

from langchain_core.messages import HumanMessage
from langchain_core.stores import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver
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

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable":{"thread_id":"325893475"}}

graph.invoke({"messages": [HumanMessage("你好，我是老王")]},config = config)
graph.invoke({"messages": [HumanMessage("从现在开始，你是小王")]},config = config)
res = graph.invoke({"messages": [HumanMessage("我是谁，你是谁")]},config = config)

print(res["output"])

print("------------------------------------")
for msg in res["messages"]:
    msg.pretty_print()