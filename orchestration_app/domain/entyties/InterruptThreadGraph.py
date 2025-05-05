from langgraph.graph import StateGraph


class InterruptThreadGraph:
    """사용자 세션과 그래프 클래스"""

    def __init__(self, thread_id: str, graph: StateGraph):
        self.thread_id = thread_id
        self.graph = graph
