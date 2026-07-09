import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

_model: ChatOpenAI | None = None


def get_model() -> ChatOpenAI:
    """获取模型单例，首次调用时创建，后续复用同一实例"""
    global _model
    if _model is None:
        _model = ChatOpenAI(
            model=os.getenv("deepseek_model_name"),
            api_key=os.getenv("deepseek_api_key"),
            base_url=os.getenv("deepseek_base_url"),
        )
    return _model

def get_image_model() -> ChatOpenAI:
    """获取模型单例，首次调用时创建，后续复用同一实例"""
    global _model
    if _model is None:
        _model = ChatOpenAI(
            model=os.getenv("m_deepseek_model_name"),
            api_key=os.getenv("m_deepseek_api_key"),
            base_url=os.getenv("m_deepseek_base_url"),
        )
    return _model


if __name__ == "__main__":
    model = get_model()
    response = model.invoke("你好，请简单介绍一下你自己")
    print(response.content)
    msg = ''
    for chunk in model.stream("你好，今天天气怎么样？"):
        if chunk.content:
            msg += chunk.content
        print(msg)
