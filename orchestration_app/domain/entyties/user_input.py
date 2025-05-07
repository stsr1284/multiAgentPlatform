from pydantic import BaseModel, Field


class UserInput(BaseModel):
    thread_id: str = Field(..., description="사용자 thread_id")
    query: str = Field(..., description="사용자 요청")


class OrchestrationInput(UserInput):
    agent_list: list[str] = Field(..., description="사용할 에이전트 목록")
    orchestrator_type: str = Field(..., description="사용할 오케스트레이터 종류")
