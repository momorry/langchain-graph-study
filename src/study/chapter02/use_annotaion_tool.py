from typing import Literal

from langchain_core.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import BaseModel, Field


@tool(description="获取城市的天气")
def get_weather(city: str = "广州"):
    return f"{city}的温度为24摄氏度"


class WeatherTool(BaseModel):
    city: str = Field(description="城市的名称", default="广州")
    dt: str = Field(description="时间")
    unit: Literal['摄氏度','华氏度']
    include_forecast: bool = Field(default=False, description="是否包含未来5天的天气")

@tool(args_schema=WeatherTool)
def get_weather2(city: str = "广州"):
    """
    获取城市的天气
    """
    return f"{city}的温度为24摄氏度"

json_schema3 = {'name': 'get_weather2', 'description': '获取城市的天气', 'parameters': {'properties': {'city': {'default': '广州', 'description': '城市的名称', 'type': 'string'}, 'dt': {'description': '时间', 'type': 'string'}, 'unit': {'enum': ['摄氏度', '华氏度'], 'type': 'string'}, 'include_forecast': {'default': False, 'description': '是否包含未来5天的天气', 'type': 'boolean'}}, 'required': ['dt', 'unit'], 'type': 'object'}}

@tool(args_schema=json_schema3)
def get_weather3(city, dt, unit, include_forecast):
    return f"{city}{dt}的温度为24{unit}"

if __name__ == "__main__":
    print(convert_to_openai_tool(get_weather))
    print(convert_to_openai_tool(get_weather2))
    print(convert_to_openai_tool(get_weather3))
