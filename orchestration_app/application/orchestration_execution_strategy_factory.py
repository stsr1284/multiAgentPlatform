from orchestration_app.domain.strategies.InvokeStrategy import InvokeStrategy
from orchestration_app.domain.strategies.AInvokeStrategy import AInvokeStrategy
from orchestration_app.domain.strategies.StreamStrategy import StreamStrategy

class StrategyFactory:
    def __init__(self, service):
        self.service = service

    def get_strategy(self, strategy_type: str):
        match strategy_type:
            case "invoke":
                return InvokeStrategy(self.service)
            case "ainvoke":
                return AInvokeStrategy(self.service)
            case "stream":
                return StreamStrategy(self.service)
            case _:
                raise ValueError(f"Unknown strategy: {strategy_type}")
