from langchain_openai import ChatOpenAI
from utils.config import settings

llmModel = ChatOpenAI(
    name="gpt-4o",
    model="gpt-4o",
    temperature=0,
    api_key=settings.OPENAI_API_KEY,
)


async def register(registry):
    await registry.register(llmModel)
