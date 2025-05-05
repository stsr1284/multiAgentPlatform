from pydantic import BaseModel, Field


class UserInput(BaseModel):
    id: str = Field(..., description="User ID")
    session: str = Field(..., description="Session")
    query: str = Field(..., description="User query")
    agent_list: list[str] = Field(..., description="List of agents to use")
    orchestrator_type: str = Field(
        "SupervisorOrchestrationBuilder", description="Type of orchestrator to use"
    )
