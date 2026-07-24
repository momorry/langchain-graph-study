from operator import add
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Overwrite


class StudyState(TypedDict):
    name: Annotated[str, add]
    age: Annotated[int, add] #当存在并行节点时，必须指定reducer函数


def node_01(state: StudyState) -> StudyState:
    name = state["name"] + " hi"
    for k, v in state.items():
        print('node01-----', k, v)
    return {
        "name": name,
        "age": 11
    }


def node_02(state: StudyState) -> StudyState:
    name = state["name"] + " hi"
    for k, v in state.items():
        print('node02-----', k, v)
    return {
        "name": name,
        "age": 12
    }


# 在节点中遍历state
def node_03(state: StudyState) -> StudyState:
    for k, v in state.items():
        print('node03-----', k, v)
    return {
        "name": Overwrite("wang wu "),  # 仅在当前节点使用覆盖操作，并不使用state里面定义的add
        "age": 13
    }


def node_04(state: StudyState) -> StudyState:
    for k, v in state.items():
        print('node04-----', k, v)
    return {
        "name": "la qi",
        "age": 15
    }


graph_builder = StateGraph(state_schema=StudyState)

graph_builder.add_node(node_01)
graph_builder.add_node(node_02)
graph_builder.add_node(node_03)
graph_builder.add_node(node_04)

graph_builder.add_edge(START, "node_01")
graph_builder.add_edge("node_01", "node_02")
graph_builder.add_edge("node_01", "node_03")
graph_builder.add_edge("node_02", "node_04")
graph_builder.add_edge("node_03", "node_04")
graph_builder.add_edge("node_04", END)

graph = graph_builder.compile()

res = graph.invoke({"name": "", "age": 0})
print(res)
