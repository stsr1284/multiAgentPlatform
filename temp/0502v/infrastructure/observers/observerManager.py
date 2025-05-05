from domain.interfaces.Observer import Observer
from typing import List

# 옵저버 관리 클래스
class ObserverManager:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    async def notify_observers(self, data: str) -> None:
        for observer in self._observers:
            await observer.update(data)
