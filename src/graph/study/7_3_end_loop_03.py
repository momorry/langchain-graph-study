from typing import TypedDict, Literal

from langchain_core.runnables import RunnableConfig
from langgraph.constants import END, START
from langgraph.errors import GraphRecursionError
from langgraph.graph.state import  StateGraph
from langgraph.managed.is_last_step import RemainingSteps
from loguru import logger

class OverAllState(TypedDict):
   pass


def loop_node(state: OverAllState, config:RunnableConfig) -> OverAllState:
    cur_step = config['metadata']['langgraph_step']
    logger.info(f"cur_step: {cur_step}")



builder = StateGraph(state_schema=OverAllState)

builder.add_node("loop_node", loop_node)
builder.add_edge(START, "loop_node")
builder.add_edge("loop_node", "loop_node")

graph = builder.compile()
try:
    res = graph.invoke({}, config=RunnableConfig(recursion_limit=5))
    print(res)
except GraphRecursionError as e:
    logger.error("超过限制步数，停止")

