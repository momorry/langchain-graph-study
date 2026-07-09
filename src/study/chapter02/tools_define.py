from langchain_core.utils.function_calling import convert_to_openai_tool


def get_weather(city):
    """
    获取城市的天气
    Args:
        city: 城市名称
    Returns: 城市的温度
    """
    return f"{city}的温度为24摄氏度"


if __name__ == "__main__":
   print(convert_to_openai_tool(get_weather))

