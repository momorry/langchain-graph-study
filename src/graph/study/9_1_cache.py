import time
from operator import add
from typing import TypedDict, Annotated

from langgraph.cache.memory import InMemoryCache
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy
from loguru import logger


class OverallState(TypedDict):
    user: str
    cnt: Annotated[int, add]


def node_a(state: OverallState) -> OverallState:
    logger.info(f"{state['user']}开始计算")
    time.sleep(3)
    state['cnt'] += 1
    logger.info(f"{state['user']}计算完成 cnt={state['cnt']}")
    return state


builder = StateGraph(state_schema=OverallState)
builder.add_node(node_a, cache_policy=CachePolicy(ttl=60))
builder.add_edge(START, "node_a")
builder.add_edge("node_a", END)
graph = builder.compile(cache=InMemoryCache())

res1 = graph.invoke({"user": "zhangsan", "cnt": 0})
print("res1=", res1)
res2 = graph.invoke({"user": "zhangsan", "cnt": 0})
print("res2=", res2)
res3 = graph.invoke({"user": "lisi", "cnt": 0})
print("res3=", res3)
