import base64
from typing import Any
from pathlib import Path

from langchain_core.messages import HumanMessage

from src.study import PROJECT_ROOT
from src.study.base.model.chat_model import  get_image_model


def chat_with_model(prompt: str, image_path: str = "", use_base64: bool = False) -> str | list[str | Any]:
    """与模型进行对话"""
    model = get_image_model()
    h_msg = choice(use_base64, prompt, image_path)
    response = model.invoke([h_msg])
    return response.content

def encode_image(image_path: str) -> str:
    """将图片文件编码为 base64 字符串，相对路径基于项目根目录解析"""
    path = Path(image_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _detect_mime_type(image_path: str) -> str:
    """根据文件后缀推断 MIME 类型"""
    suffix = Path(image_path).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_map.get(suffix, "image/png")

def choice(use_base64: bool, prompt: str, image_path: str = "") -> HumanMessage:
    if not use_base64:
        h_msg = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url":
                {"url": "https://c.53326.com/d/file/bigpic/20200519/5t0x4zrqc4a.jpg", "detail": "auto"}
             }
        ])
    else:
        b64_data = encode_image(image_path)
        mime_type = _detect_mime_type(image_path)
        h_msg = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url":
                {"url": f"data:{mime_type};base64,{b64_data}"}
             }
        ])
    return h_msg

if __name__ == "__main__":
    # 方式1：使用 URL 图片
    # print(chat_with_model("图片里面有什么"))

    # 方式2：使用本地图片 base64 编码
    print(chat_with_model("图片里面有什么", image_path="src/resource/data/test.png", use_base64=True))
