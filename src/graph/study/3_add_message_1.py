from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import add_messages
from rich import print as rprint

messages_left = [
    SystemMessage("你是一个大学老师", id=1),
    HumanMessage("为什么圆周率无法算尽", id=2),
    AIMessage("不知道啊1", id=3)
]

messages_right = [
    HumanMessage("如何理解直角三角函数", id=1),
    AIMessage("不知道啊2", id=2),
    HumanMessage("如何理解直角三角函数", id=3),
    AIMessage("不知道啊3", id=4)
]
# 内置reducer函数 add_messages 仅根据id值是否一样进行覆盖 
res = add_messages(messages_left, messages_right)

rprint(res)
