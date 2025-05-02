from langchain_openai import ChatOpenAI

llmModel = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)


async def register(registry):
    await registry.register(llmModel)
