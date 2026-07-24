from typing import TypedDict, Literal

from langchain_core.messages import HumanMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.types import Command

from study.base.model.chat_model import get_model

# 初始化大语言模型
model = get_model()


# ==================== 状态定义 ====================

# 1. 全局状态 (OverAllState)：整个图运行期间共享的状态
#    - topic: 用户输入的主题
#    - pome: 存储生成的七言绝句
#    - ci_pome: 存储生成的词
#    - joke: 存储生成的笑话
class OverAllState(TypedDict):
    topic: str
    pome: str
    joke: str
    content_type: Literal['pome', 'joke']
    content_chinese: str


def router(state: OverAllState) -> Command[Literal['pome_node', 'joke_node', '__end__']]:
    if state['content_type'] == 'pome':
        return Command(update={'content_chinese': '七言绝句'}, goto='pome_node')
    elif state['content_type'] == 'joke':
        return Command(update={'content_chinese': '一个笑话'}, goto='joke_node')
    else:
        return Command('__end__', state)


# 定义节点
def pome_node(state: OverAllState) -> OverAllState:
    prompt = "请生成一首关于{}的{}".format(state['topic'], state['content_chinese'])
    content = model.invoke([HumanMessage(prompt)]).content
    return {
        'pome': content
    }


def joke_node(state: OverAllState) -> OverAllState:
    prompt = "请生成一首关于{}的{}".format(state['topic'], state['content_chinese'])
    content = model.invoke([HumanMessage(prompt)]).content
    return {
        'joke': content
    }


# 定义图
builder = StateGraph(state_schema=OverAllState)
builder.add_node('router', router)
builder.add_node('pome_node', pome_node)
builder.add_node('joke_node', joke_node)

builder.add_edge(START, 'router')
builder.add_edge('pome_node', END)
builder.add_edge('joke_node', END)

graph = builder.compile()
res = graph.invoke({'topic': '山峦', 'content_type': 'pome'})
print(res)
print("===" * 50)
res2 = graph.invoke({'topic': '山峦', 'content_type': 'joke'})
print(res2)

#总结：通过command可以替代add_conditional_edges来实现分支跳转路由