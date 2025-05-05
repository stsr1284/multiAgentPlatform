from langchain.tools import tool
from langgraph.types import interrupt


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""

    response = interrupt("안뇽 나는 interrupt를 호출할고얌!!")
    print("*******add response:", response)
    return a + b


async def register(registry):
    await registry.register(add)
