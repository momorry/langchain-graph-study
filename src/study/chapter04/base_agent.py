from langchain.agents import create_agent
from langchain_core.tools import tool
from rich import print as rprint

from study.base.model.chat_model import get_model


@tool(description="获取城市的天气")
def get_weather(city):
    return f"{city}的温度为24摄氏度"


agent = create_agent(
    model=get_model(),
    tools=[get_weather]
)

resp = agent.invoke({
    "messages":[("system","你是一个天气查询助手"),("human","今天长沙的天气怎么样")]
})

rprint(resp)