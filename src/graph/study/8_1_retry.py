from typing import TypedDict, Literal

from httpx import HTTPError
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy, Command
from loguru import logger


class EmptyState(TypedDict):
    cnt: int


def node_a(state: EmptyState) -> EmptyState:
    state['cnt']+=1
    logger.info(f"node_a, cnt{state['cnt']}")
    if state.get("cnt") < 3:
        raise HTTPError("错误")
    return state


builder = StateGraph(state_schema=EmptyState)
builder.add_node(node_a, retry_policy=RetryPolicy(max_attempts=5))
builder.add_edge(START, "node_a")
builder.add_edge("node_a", END)

graph = builder.compile()

try:
    graph.invoke({"cnt": 0})
except HTTPError as e:
    logger.error("HTTPError")
