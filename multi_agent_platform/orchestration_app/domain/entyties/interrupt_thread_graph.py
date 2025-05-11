from langgraph.graph.graph import CompiledGraph


class InterruptThreadGraph:
    """사용자 세션과 그래프 클래스"""

    def __init__(self, thread_id: str, graph: CompiledGraph):
        self.thread_id = thread_id
        self.graph = graph
