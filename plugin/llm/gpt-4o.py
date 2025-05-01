from langchain_openai import ChatOpenAI

llmModel = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=,
)


async def register_llm(registry):
    await registry.register(llmModel)
