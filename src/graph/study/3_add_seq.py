
from operator import add
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class StudyState(TypedDict):
    name: Annotated[str, add]
    age: int


def node_01(state: StudyState) -> StudyState:
    state["name"] = "zhang san"
    name = state["name"] + " hi"
    return {
        "name":name,
        "age":11
    }

def node_02(state: StudyState) -> StudyState:
    state["name"] = "li si"
    name = state["name"] + " hi"
    return {
        "name":name,
        "age":12
    }

graph_builder = StateGraph(state_schema = StudyState)

# graph_builder.add_node("node_01",node_01)
# graph_builder.add_node("node_02", node_02)
# graph_builder.add_edge(START, "node_01")
# graph_builder.add_edge("node_01", "node_02")
# graph_builder.add_edge("node_02", END)

graph_builder.add_edge(START, "node_01")
graph_builder.add_sequence([node_01,node_02])
graph_builder.add_edge("node_02", END)

graph = graph_builder.compile()

res = graph.invoke({"name":"","age":0})
print(res)


