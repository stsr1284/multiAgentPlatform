from .BaseBuilder import BaseBuilder
from pydantic import ValidationError
from orchestration_app.shared.loggin_config import logger


class BaseOrchestratorBuilder(BaseBuilder):
    async def __call__(self, **kwargs):
        try:
            input = BaseOrchestartionBuilderInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        return await self.build(input)
