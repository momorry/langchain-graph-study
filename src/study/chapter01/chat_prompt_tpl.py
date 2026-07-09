from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.study.base.model.chat_model import get_model

# 元组列表
def chat_prompt_tpl() -> PromptValue :
    """与模型进行对话"""
    c_tpl = ChatPromptTemplate.from_messages([
        ("system", "你是一个风趣幽默的AI助手"),
        ("human", "Hello, how are you?"),
        ("ai", "I'm doing well, thanks!"),
        ("human","{prompt}"),
    ])
    response = c_tpl.invoke({"prompt":"你好，请简单介绍一下你自己"})
    return response
# 元组列表
def chat_prompt_tpl_format() -> list[BaseMessage]:
    """与模型进行对话"""
    c_tpl = ChatPromptTemplate.from_messages([
        ("system", "你是一个风趣幽默的AI助手"),
        ("human", "Hello, how are you?"),
        ("ai", "I'm doing well, thanks!"),
        ("human","{prompt}"),
    ])
    response = c_tpl.format_messages(prompt = "你好，请简单介绍一下你自己")
    return response

def chat_prompt_tpl_format_dict() -> list[BaseMessage]:
    """与模型进行对话"""
    c_tpl = ChatPromptTemplate.from_messages([
        {"role": "system", "content": "你是一个风趣幽默的AI助手"},
        {"role": "human", "content": "{prompt}"},
    ])
    response = c_tpl.format_messages(prompt = "你好，请简单介绍一下你自己")
    return response

def chat_prompt_tpl_format_clazz() -> list[BaseMessage]:
    """与模型进行对话"""
    s = SystemMessagePromptTemplate.from_template("你是一个风趣幽默的AI助手")
    human = HumanMessagePromptTemplate.from_template("{prompt}")
    c_tpl = ChatPromptTemplate.from_messages([
        s,
        human
    ])
    response = c_tpl.format_messages(prompt="你好，请简单介绍一下你自己")
    return response

if __name__ == "__main__":
    print(type(chat_prompt_tpl()))
    model = get_model()
    # res = model.invoke(chat_prompt_tpl())
    # print(res.content)
    # print("------------")
    # res2 = model.invoke(chat_prompt_tpl_format())
    # print(type(chat_prompt_tpl_format()))
    # print(res2.content)
    # print("------------")
    # res3 = model.invoke(chat_prompt_tpl_format_dict())
    # print(type(chat_prompt_tpl_format_dict()))
    # print(res3.content)
    # print("------------")
    res4= model.invoke(chat_prompt_tpl_format_clazz())
    print(res4.content)
