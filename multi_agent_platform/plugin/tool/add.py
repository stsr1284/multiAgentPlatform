from langchain.tools import tool
from langgraph.types import interrupt


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""

    response = interrupt("정말 하시겠습니다? yes/no")
    if response == "yes":
        print("*******add response:", response)
        return a + b
    else:
        print("*******add response:", response)
        return 0


async def register(registry):
    await registry.register(add)
