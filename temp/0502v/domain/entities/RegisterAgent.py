from pydantic import BaseModel
from typing import Any

class RegisterAgent(BaseModel):
    type: str
    config: dict[str, Any]
    # id: str
    # name: str
    # description: str
    # endpoint: str
    # status: str = "active"
