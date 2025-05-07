from langchain.tools import tool
from langgraph.types import interrupt


@tool
def get_wepone(hotel_name: str):
    """가위바위보 게임을 위한 무기 선택 도구입니다."""
    response = interrupt(
        f"Trying to call `book_hotel` with args {{'hotel_name': {hotel_name}}}. "
        "Please approve or suggest edits."
    )
    print("book_hotel response:", response)
    return f"Successfully booked a stay at {hotel_name}."


async def register(registry):
    await registry.register(get_wepone)
