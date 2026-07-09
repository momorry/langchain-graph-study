from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool

from study.base.model.chat_model import get_model


@tool(description="获取城市的天气")
def get_weather(city):
    return f"{city}的温度为24摄氏度"

def use_tool():
    model = get_model()
    model_tool = model.bind_tools([get_weather])
    response = model_tool.invoke("广州的天气如何？")
    if response.tool_calls:
        print("AI: 调用工具", response.tool_calls)
    else:
        print("AI: 直接回答", response.content)

def use_tool1() :
    messages: list[BaseMessage] = [HumanMessage("广州今天的天气怎么样？")]

    model = get_model()
    model_tool = model.bind_tools([get_weather])
    res = model_tool.invoke(messages)
    messages.append(res)

    if res.tool_calls:
        print("AI1: 调用工具", res.tool_calls)
    else:
        print("AI1: 直接回答", res.content)

    if res.tool_calls:
        for tool_call in res.tool_calls:
            if tool_call.get("name") == "get_weather":
                t_res = get_weather.invoke(tool_call)
                messages.append(t_res)

    res2 = model_tool.invoke(messages)
    if res2.tool_calls:
        print("AI2: 调用工具", res2.tool_calls)
    else:
        print("AI2: 直接回答", res2.content)


if __name__ == "__main__":
   # use_tool()
   use_tool1()
