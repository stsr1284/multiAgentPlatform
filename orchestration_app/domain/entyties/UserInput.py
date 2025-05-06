from pydantic import BaseModel, Field


class UserInput(BaseModel):
    thread_id: str = Field(..., description="Session")
    query: str = Field(..., description="User query")


class OrchestrationInput(UserInput):
    agent_list: list[str] = Field(..., description="List of agents to use")
    orchestrator_type: str = Field(
        "SupervisorOrchestrationBuilder", description="Type of orchestrator to use"
    )
