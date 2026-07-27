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
    if state.get("cnt") < 5:
        raise HTTPError("错误")
    return state

def node_b(state: EmptyState) -> EmptyState:
    logger.info(f"node_b")
    return state

def handler_a(state: EmptyState) -> Command[Literal['node_b']]:
    return Command(update={"cnt": 0}, goto="node_b")

builder = StateGraph(state_schema=EmptyState)
#最多重试4次，每次重试时间间隔为0.5*backoff_factor,当重试次数耗尽后，跳转到node_b
builder.add_node(node_a, retry_policy=RetryPolicy(max_attempts=4, backoff_factor=1),error_handler=handler_a)
builder.add_node(node_b)
builder.add_edge(START, "node_a")
builder.add_edge("node_a", END)

graph = builder.compile()

try:
    graph.invoke({"cnt": 0})
except HTTPError as e:
    logger.error("HTTPError")
