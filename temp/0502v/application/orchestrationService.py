from pydantic import Field
from orchestration_app.domain.interfaces.AgentRepositoryInterface import (
    AgentRepositoryInterface,
)
from orchestration_app.shared.loggin_config import logger  # test
from orchestration_app.domain.entities.BaseAgent import BaseAgent


class OrchestrationService:
    agentRepository: AgentRepositoryInterface = Field(
        default_factory=AgentRepositoryInterface, description="agentRepository"
    )

    def __init__(
        self,
        agentRepository: AgentRepositoryInterface,
    ):
        self.agentRepository = agentRepository

    async def execute(
        self,
        session: str,
        user_id: str,
        query: str,
        agent_list: list[str],
        orchestrator_type: str,
    ):
        try:
            all_agents = await self.agentRepository.get_agents()
            if not all_agents:
                logger.warning("No agents found.")
                raise ValueError("No agents available.")

            selected_agents = [all_agents[key] for key in agent_list]
            if not selected_agents:
                logger.warning("No matching agents found.")
                raise ValueError("No matching agents found.")

        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            raise
