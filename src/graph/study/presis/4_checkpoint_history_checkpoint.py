from datetime import datetime

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

config = {"configurable":{"thread_id":"2342342"}}

#durability持久化模式，exit,async,sync

graph.invoke({"messages": [HumanMessage("你好，我是老王")]},config = config,durability="async")
graph.invoke({"messages": [HumanMessage("从现在开始，你是小王")]},config = config,durability="async")
res = graph.invoke({"messages": [HumanMessage("我是谁，你是谁")]},config = config,durability="async")

print(res["output"])

print("------------------------------------")
for msg in res["messages"]:
    msg.pretty_print()

print("------------历史检查点")
his_checkpoints = list(graph.get_state_history(config=config))

#对象类型取属性直接.属性名，dict取属性使用[]
for hc in his_checkpoints:
    for ms in hc.values["messages"]:
        ak = ms.additional_kwargs
        # 往ak里面添加create_at字段，值为当前系统时间
        ak["create_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(his_checkpoints)

#最新的一步检查点
last_check_point = graph.get_state(config=config)

#如果希望查看某个历史检查点，可以在 **`configurable`** 中额外传入 **`checkpoint_id`**
target_config = {
    "configurable": {
        "thread_id": "123",
        "checkpoint_id": "某个历史 checkpoint_id"
    }
}

snapshot = graph.get_state(config=target_config)
print(snapshot)