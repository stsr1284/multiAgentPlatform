from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import settings

gemini = ChatGoogleGenerativeAI(
    name="gemini-2.5-pro-preview-05-06",
    model="gemini-2.5-pro-preview-05-06",
    temperature=0,
    api_key=settings.GOOGLE_API_KEY,
)


async def register(registry):
    await registry.register(gemini)
