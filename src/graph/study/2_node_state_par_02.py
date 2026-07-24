from operator import add
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from study.base.model.chat_model import get_model



class StudyState(TypedDict):
    topic: Annotated[str,add]
    stud1: Annotated[str,add]
    stud2: Annotated[str,add]


def node_01(state: StudyState) -> StudyState:
    model = get_model()
    art = model.invoke(f"基于这个主题{state['topic']}撰写一篇100字的文章")
    return {"stud1": art.content}

def node_02(state: StudyState) -> StudyState:
    model = get_model()
    art = model.invoke(f"基于这个主题{state['topic']}撰写一篇100字的文章")
    return {"stud2": art.content}


graph_builder = StateGraph(state_schema=StudyState)

graph_builder.add_node(node_01)
graph_builder.add_node(node_02)

graph_builder.add_edge(START, "node_01")
graph_builder.add_edge(START, "node_02")
graph_builder.add_edge("node_01", END)
graph_builder.add_edge("node_02", END)

graph = graph_builder.compile()

res = graph.invoke({"topic": "红星照耀中国"})

print(res)
