from langchain_anthropic import ChatAnthropic
from utils.config import settings

model = ChatAnthropic(
    name="calude-3-7-sonnet",
    model="claude-3-7-sonnet-latest",
    api_key=settings.ANTHROPIC_API_KEY,
)


async def register(registry):
    await registry.register(model)
