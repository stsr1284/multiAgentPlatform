from langchain_openai import ChatOpenAI

llmModel = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


async def register(registry):
    await registry.register(llmModel)
