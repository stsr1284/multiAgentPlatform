import importlib.util
import inspect
import os
from pathlib import Path
from orchestration_app.domain.registry.ToolRegistry import ToolRegistry
from orchestration_app.shared.loggin_config import logger


def is_tool_function(func):
    """@tool 데코레이터가 붙은 함수인지 확인."""
    # 가정: @tool 데코레이터가 함수에 __tool__ 속성을 추가

    # 메타데이터 표준출력
    print(f"Function Name: {func.__name__}")
    print(f"Function Docstring: {func.__doc__}")
    print(f"Function Annotations: {func.__annotations__}")
    return hasattr(func, "__tool__") or (
        hasattr(func, "__wrapped__") and hasattr(func.__wrapped__, "__tool__")
    )


def load_tools_from_file(file_path: str):
    """단일 파일에서 @tool 함수를 로드."""
    try:
        # 파일 이름에서 모듈 이름 생성
        module_name = Path(file_path).stem
        print(f"Module name: {module_name}")
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        print(f"Spec: {spec}")
        if spec is None:
            logger.warning(f"Cannot create spec for {file_path}")
            return []

        module = importlib.util.module_from_spec(spec)
        print(f"Module: {module}")
        spec.loader.exec_module(module)

        # 모듈 내 모든 멤버를 검사
        tools = []
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            print(f"Inspecting {name}: {obj}")
            if is_tool_function(obj):
                print(f"Found tool function: {name}")
                tools.append(obj)
                logger.info(f"Found tool: {name} in {file_path}")
        return tools
    except Exception as e:
        logger.error(f"Error loading tools from {file_path}: {e}")
        return []


def register_tools_from_directory(directory: str) -> ToolRegistry:
    """지정된 디렉토리에서 모든 @tool 함수를 찾아 ToolRegistry에 등록."""
    tool_registry = ToolRegistry()
    directory_path = Path(directory)
    print(f"Directory path: {directory_path}")

    if not directory_path.exists():
        logger.error(f"Directory {directory} does not exist")
        return tool_registry

    # .py 파일 순회
    for file_path in directory_path.rglob("*.py"):
        if file_path.name.startswith("__"):  # __init__.py 등 제외
            continue
        print(f"Processing file: {file_path}")
        tools = load_tools_from_file(file_path)
        for tool in tools:
            tool_registry.register(tool)
            logger.info(f"Registered tool: {tool.__name__}")

    return tool_registry


# 사용 예시
if __name__ == "__main__":
    # 디렉토리에서 모든 @tool 함수를 찾아 등록
    tool_registry = register_tools_from_directory("./tools")

    # 등록된 도구 확인
    try:
        research_tool = tool_registry.get("research_tool")
        print(research_tool("AI"))  # 예: Researching the topic: AI
        search_urls_tool = tool_registry.get("search_urls")
        print(
            search_urls_tool(["http://example.com"], 1)
        )  # 예: Searching the following URLs: ['http://example.com']
    except ValueError as e:
        print(f"Error: {e}")
