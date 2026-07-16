from enum import Enum
from typing import Optional, Literal

from pydantic import BaseModel, Field, ConfigDict

from study.base.model.chat_model import get_model

class TeachingLevel(str, Enum):
    low = "低"
    mid = "中"
    high = "非常高"


class Person(BaseModel):
    name: str = Field(description="姓名")
    age: Optional[int] = Field(default=None, description="年龄")
    occupation: str = Field(description="职业")
    occupation_level: Literal["低","中","高"] = Field( description="职业等级")
    teaching_level: Literal["低","中","高"] = Field(description="教学水平")


str_model = get_model().with_structured_output(Person, method="json_mode")

res = str_model.invoke("请以json格式回答：张三是一名教师,职业等级高，教学水平高")

print(res)
print(type(res))