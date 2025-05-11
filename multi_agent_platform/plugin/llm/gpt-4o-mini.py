from langchain_openai import ChatOpenAI
from utils.config import settings


llmModel = ChatOpenAI(
    name="gpt-4o-mini",
    model="gpt-4o-mini",
    temperature=0,
    api_key=settings.OPENAI_API_KEY,
)


async def register(registry):
    await registry.register(llmModel)
