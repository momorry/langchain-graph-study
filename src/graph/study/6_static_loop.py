from random import randint
from typing import Literal

from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph

from study.base.model.chat_model import get_model


@tool(description="获取城市的天气")
def get_weather(city):
    return f"{city}的温度为24摄氏度"


@tool(description="查询特定领域的当日热点")
def get_news(domain: Literal["AI", "食品安全"]):
    if domain == "AI":
        return "Anthropic 发布了 Claude Opus-4.8，但通过 API 用中文向它发送“你是谁？”时，大多数情况下返回的却是“Qwen”或“Deepseek”。"
    elif domain == "食品安全":
        return "双汇发展子公司猪肉产品被抽检出抗生素超标37.5倍"
    else:
        return "未知的新闻领域"


model = get_model()
model_with_tool = model.bind_tools([get_weather, get_news])


class OverAllState(MessagesState):
    user_input: str
    final_output: str


def input_node(state: OverAllState) -> OverAllState:
    return {"messages": [HumanMessage(state["user_input"])]}


def llm_node(state: OverAllState) -> OverAllState:
    ai_msg = model_with_tool.invoke(state['messages'])
    return {"messages": ai_msg}


def tool_node(state: OverAllState) -> OverAllState:
    messages = state['messages']
    ai_msg = messages[-1]
    tool_calls = ai_msg.tool_calls
    # 表示失败率为0.6
    fail_prob = 6

    for tool_call in tool_calls:
        if tool_call.get("name") == "get_weather":
            if randint(0, 9) < fail_prob:
                messages.append(ToolMessage(content="网络波动，请重试", tool_call_id=tool_call['id']))
            else:
                messages.append(get_weather.invoke(tool_call))
        elif tool_call["name"] == "get_news":
            if randint(0, 9) < fail_prob:
                messages.append(ToolMessage(
                    content="网络波动,调用失败,请重试",
                    tool_call_id=tool_call["id"]
                ))
            else:
                messages.append(get_news.invoke(tool_call))
        else:
            messages.append(ToolMessage(
                content="工具名称错误,调用失败,请重试",
                tool_call_id=tool_call["id"]
            ))
    return {"messages": messages}


def output_node(state: OverAllState) -> OverAllState:
    return {
        "final_output": state["messages"][-1].content
    }


def router(state: OverAllState) -> Literal["tool_node", "output_node"]:
    messages = state['messages']
    last_msg = messages[-1]
    if last_msg.tool_calls:
        return "tool_node"
    return "output_node"


# 3. 构建图
builder = StateGraph(state_schema=OverAllState)
builder.add_node("input_node", input_node)
builder.add_node("llm_node", llm_node)
builder.add_node("tool_node", tool_node)
builder.add_node("output_node", output_node)

builder.add_edge(START, "input_node")
builder.add_edge("input_node", "llm_node")
builder.add_conditional_edges("llm_node", router)
builder.add_edge("tool_node", "llm_node")
builder.add_edge("output_node", END)

graph = builder.compile()

ai_res = graph.invoke({
    "user_input": "查询今天的上海天气和AI新闻热点",
    "messages": [SystemMessage("如果工具调用失败,必须重新调用直到成功为止")]
})

print("user_input:", ai_res["user_input"])
print("final_output:", ai_res["final_output"])
for msg in ai_res["messages"]:
    msg.pretty_print()
