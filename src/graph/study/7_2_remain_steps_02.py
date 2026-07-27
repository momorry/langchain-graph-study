from typing import TypedDict, Literal

from langchain_core.runnables import RunnableConfig
from langgraph.constants import END, START
from langgraph.graph.state import  StateGraph
from langgraph.managed.is_last_step import RemainingSteps
from loguru import logger

class OverAllState(TypedDict):
    remain_steps: RemainingSteps


def loop_node(state: OverAllState, config:RunnableConfig) -> OverAllState:
    cur_step = config['metadata']['langgraph_step']
    remain_steps = state.get('remain_steps')
    logger.info(f"cur_step: {cur_step}, remain_steps: {remain_steps}")

def router(state: OverAllState) -> Literal['loop_node', END]:
    remain_steps = state.get('remain_steps')
    if remain_steps < 3:
        return END
    return 'loop_node'


builder = StateGraph(state_schema=OverAllState)

builder.add_node("loop_node", loop_node)
builder.add_edge(START, "loop_node")
builder.add_conditional_edges("loop_node", router)

graph = builder.compile()
res = graph.invoke({}, config=RunnableConfig(recursion_limit=5))

print(res)
