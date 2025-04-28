class OrchestratorFactory:
    ORCHESTRATORS = {
        "langgraph": LangGraphOrchestrator,
        "custom": CustomOrchestrator
    }

    def __init__(self, redis_client: redis.Redis = Depends(lambda: redis.Redis(host="redis.example.com", port=6379, db=0))):
        self.redis_client = redis_client
        self.orchestrators: Dict[str, OrchestratorInterface] = {}

    async def create_orchestrator(
        self,
        session: str,
        orchestrator_type: str,
        tool_list: ToolListProvider,
        broker: BrokerInterface
    ) -> OrchestratorInterface:
        if session in self.orchestrators:
            logger.info(f"Reusing orchestrator for session: {session}")
            return self.orchestrators[session]

        cls = self.ORCHESTRATORS.get(orchestrator_type)
        if not cls:
            raise ValueError(f"Unknown orchestrator type: {orchestrator_type}")

        memory = Memory(session_id=session)
        orchestrator = cls(tool_list, broker, memory)
        self.orchestrators[session] = orchestrator
        await self.redis_client.set(f"orchestrator:{session}", orchestrator_type, ex=3600)
        logger.info(f"Created {orchestrator_type} orchestrator for session: {session}")
        return orchestrator