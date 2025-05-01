from langchain_openai import ChatOpenAI

llmModel = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key="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",
)


async def register(registry):
    await registry.register(llmModel)
