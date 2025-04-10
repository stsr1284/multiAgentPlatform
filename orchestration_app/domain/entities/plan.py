class Plan:
    def __init__(self, steps: list):
        self.steps = steps

    @classmethod
    def create_plan(cls, query: str):
        # 단순 예시: 쿼리에 따라 step을 결정
        steps = [{"agent": "plan_execute_agent", "task": query}]
        return cls(steps=steps)
