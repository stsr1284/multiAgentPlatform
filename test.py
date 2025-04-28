from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Callable
from enum import Enum
import json
import os
import importlib.util
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent, create_openai_tools_agent
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 에이전트 타입 정의
class AgentType(str, Enum):
    SUPERVISOR = "supervisor"
    REACT = "react"
    TOOL_CALLING = "tool_calling"
    PLANE_EXECUTE = "plane_execute"
    COT = "cot"

# Pydantic 모델 정의
class BaseAgent(BaseModel):
    type: AgentType
    name: str
    description: Optional[str] = None
    config: Optional[Dict[str, Union[str, int]]] = None

class ReactAgent(BaseAgent):
    type: AgentType.REACT = Field(default=AgentType.REACT, alias="type")
    llm: str
    tools: List[str]
    prompt: Optional[str] = None

class ToolCallingAgent(BaseAgent):
    type: AgentType.TOOL_CALLING = Field(default=AgentType.TOOL_CALLING, alias="type")
    llm: str
    tools: List[str]
    prompt: Optional[str] = None

class PlaneExecuteAgent(BaseAgent):
    type: AgentType.PLANE_EXECUTE = Field(default=AgentType.PLANE_EXECUTE, alias="type")
    planner: Dict[str, str]
    executor: Dict[str, Union[str, List[str]]]
    replanner: Dict[str, str]

class CotAgent(BaseAgent):
    type: AgentType.COT = Field(default=AgentType.COT, alias="type")
    llm: str
    prompt: Optional[str] = None

Agent = Union[ReactAgent, ToolCallingAgent, PlaneExecuteAgent, CotAgent]

class Supervisor(BaseModel):
    model: str
    prompt: str
    agent_list: List[Agent]

class Config(BaseModel):
    supervisor: Optional[Supervisor] = None
    agent: Optional[Agent] = None

# 레지스트리 구현
class Registry:
    _registry: Dict[str, any] = {}

    @classmethod
    def register(cls, name: str, item: any) -> None:
        cls._registry[name] = item
        logger.info(f"Registered {name} in {cls.__name__}")

    @classmethod
    def get(cls, name: str) -> any:
        item = cls._registry.get(name)
        if item is None:
            logger.error(f"{name} not found in {cls.__name__}")
            raise ValueError(f"{name} not found in {cls.__name__}")
        return item

class LLMRegistry(Registry):
    pass

class ToolRegistry(Registry):
    pass

class AgentBuilderRegistry(Registry):
    pass

# 에이전트 빌더 함수
def build_react_agent(data: ReactAgent) -> AgentExecutor:
    llm = LLMRegistry.get(data.llm)
    tools = [ToolRegistry.get(tool) for tool in data.tools]
    return create_react_agent(model=llm, tools=tools, prompt=data.prompt)

def build_tool_calling_agent(data: ToolCallingAgent) -> AgentExecutor:
    llm = LLMRegistry.get(data.llm)
    tools = [ToolRegistry.get(tool) for tool in data.tools]
    return create_openai_tools_agent(model=llm, tools=tools, prompt=data.prompt)

def build_plane_execute_agent(data: PlaneExecuteAgent) -> AgentExecutor:
    # 커스텀 구현 필요
    llm = LLMRegistry.get(data.executor.get("model"))
    tools = [ToolRegistry.get(tool) for tool in data.executor.get("tools", [])]
    # 예시로 react 에이전트 사용
    return create_react_agent(model=llm, tools=tools, prompt=data.executor.get("prompt"))

def build_cot_agent(data: CotAgent) -> AgentExecutor:
    llm = LLMRegistry.get(data.llm)
    # Chain of Thought 에이전트는 커스텀 구현 필요
    return create_react_agent(model=llm, tools=[], prompt=data.prompt)

# 빌더 등록
AgentBuilderRegistry.register("react", build_react_agent)
AgentBuilderRegistry.register("tool_calling", build_tool_calling_agent)
AgentBuilderRegistry.register("plane_execute", build_plane_execute_agent)
AgentBuilderRegistry.register("cot", build_cot_agent)

# 동적 모듈 로딩
CUSTOM_MODULES_DIR = "custom_modules"

def load_custom_modules():
    if not os.path.exists(CUSTOM_MODULES_DIR):
        os.makedirs(CUSTOM_MODULES_DIR)
    for filename in os.listdir(CUSTOM_MODULES_DIR):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(CUSTOM_MODULES_DIR, filename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "register"):
                module.register()
                logger.info(f"Loaded custom module: {module_name}")

# 에이전트 빌드 함수
def build_agent(data: Agent) -> AgentExecutor:
    builder = AgentBuilderRegistry.get(data.type.value)
    return builder(data)

def build_from_config(config: Config):
    if config.supervisor:
        supervisor_data = config.supervisor
        llm = LLMRegistry.get(supervisor_data.model)
        agents = [build_agent(agent_data) for agent_data in supervisor_data.agent_list]
        # ManagementOrchestrator는 커스텀 구현 필요
        return ManagementOrchestrator(llm, agents, prompt=supervisor_data.prompt)
    elif config.agent:
        return build_agent(config.agent)
    else:
        raise ValueError("JSON must contain either 'supervisor' or 'agent'")

# FastAPI 애플리케이션
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    load_custom_modules()

@app.post("/build")
async def build(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        data = json.loads(contents)
        config = Config.parse_obj(data)
        result = build_from_config(config)
        return {"message": "Agents built successfully", "result": str(result)}
    except Exception as e:
        logger.error(f"Error building agents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_module")
async def upload_module(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(CUSTOM_MODULES_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        load_custom_modules()
        return {"message": f"Module {file.filename} uploaded and loaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading module: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 예시 ManagementOrchestrator (커스텀 구현 필요)
class ManagementOrchestrator:
    def __init__(self, model: BaseChatModel, agent_list: List[AgentExecutor], prompt: str = None):
        self.model = model
        self.agent_list = agent_list
        self.prompt = prompt
        # 그래프 또는 워크플로우 초기화 로직 추가 필요