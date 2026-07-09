from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.study.base.model.chat_model import get_model


def chat_prompt_tpl_format_placeholder1():
    """与模型进行对话"""
    msg = {"var": [("system", "你是一个风趣幽默的AI助手"), ("human", "你好，请简单介绍一下你自己")]}
    c_tpl = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="var")
    ])
    response = c_tpl.invoke(msg)
    return response


def chat_prompt_tpl_format_placeholder2():
    """与模型进行对话"""
    msg = {"history": [SystemMessage("你是一个风趣幽默的AI助手"), HumanMessage("你好，请简单介绍一下你自己")],
               "prompt": "1+1=?"}
    c_tpl = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="history"),
        ("human", "{prompt}")
    ])
    response = c_tpl.invoke(msg)
    return response


if __name__ == "__main__":
    model = get_model()
    res4 = model.invoke(chat_prompt_tpl_format_placeholder1())
    print(res4.content)
    res5 = model.invoke(chat_prompt_tpl_format_placeholder2())
    print(res5.content)
