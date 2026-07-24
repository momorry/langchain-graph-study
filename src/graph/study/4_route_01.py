from operator import add
from typing import TypedDict, Annotated, Literal

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from study.base.model.chat_model import get_model


class StudyState(TypedDict):
    topic: Annotated[str, add]
    stud1: Annotated[str, add]
    stud2: Annotated[str, add]


def node_01(state: StudyState) -> StudyState:
    model = get_model()
    msg = ''
    for chunk in model.stream(f"基于这个主题{state['topic']}撰写一篇100字的文章"):
        if chunk.content:
            msg += chunk.content
        print(f"stud1: {msg}")
    return {"stud1": msg} 


def node_02(state: StudyState) -> StudyState:
    model = get_model()
    msg = ''
    for chunk in model.stream(f"基于这个主题{state['topic']}撰写一篇100字的文章"):
        if chunk.content:
            msg += chunk.content
        print(f"stud2: {msg}")
    return {"stud2": msg}

def my_route(state: StudyState) -> Literal["node_01","node_02"]:
    if "同学1" in state["topic"]:
        return "node_01"
    else:
        return "node_02"


graph_builder = StateGraph(state_schema=StudyState)

graph_builder.add_node(node_01)
graph_builder.add_node(node_02)

graph_builder.add_conditional_edges(START, my_route)
graph_builder.add_edge("node_01", END)
graph_builder.add_edge("node_02", END)

graph = graph_builder.compile()

res = graph.invoke({"topic": "同学1来写文章，主题是：红星照耀中国"})

print(res)
