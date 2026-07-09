from typing import Any

from langchain_core.messages import HumanMessage

from src.study.base.model.chat_model import get_model


def chat_with_model(prompt: str) -> str | list[str | Any]:
    """与模型进行对话"""
    model = get_model()
    response = model.invoke([HumanMessage(content=prompt)])
    return response.content


if __name__ == "__main__":
    print(chat_with_model("你好，请简单介绍一下你自己"))