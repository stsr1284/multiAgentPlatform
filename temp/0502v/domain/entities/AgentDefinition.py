from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_core.tools.base import BaseTool
from typing import Callable, Union, Optional, Any
from pydantic import BaseModel


class AgentDefinition(BaseModel):
    type: str
    name: str
    llm: str
    prompt: Optional[str] = None
    description: Optional[str] = None
    tools: Optional[list[str]] = None
    is_custome: Optional[bool] = False
    config: Optional[dict[str, Any]] = None


# class AgentDefinition(BaseModel):
#     type: str
#     name: str
#     llm: BaseChatModel
#     prompt: Optional[str] = None
#     description: Optional[str] = None
#     tools: Optional[list[Callable[[Union[Callable, Runnable]], BaseTool]]] = None
#     is_custome: Optional[bool] = False
#     config: Optional[dict[str, Any]] = None
