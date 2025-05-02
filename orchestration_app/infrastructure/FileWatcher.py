import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio

class JsonFileWatcher(FileSystemEventHandler):
    def __init__(self, filepath: str, update_callback):
        self.filepath = filepath
        self.update_callback = update_callback

    def on_modified(self, event):
        if event.src_path.endswith(self.filepath):
            print(f"[FileWatcher] {self.filepath} 수정 감지! 업데이트 시작...")
            asyncio.create_task(self.load_json())

    async def load_json(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[FileWatcher] {self.filepath} 데이터 로드 완료")
            await self.update_callback(data)
        except Exception as e:
            print(f"[FileWatcher] JSON 로드 실패: {e}")

class FileWatcherService:
    def __init__(self, filepath: str, update_callback):
        self.filepath = filepath
        self.update_callback = update_callback
        self.event_handler = JsonFileWatcher(filepath, update_callback)
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, path=".", recursive=False)
        self.observer.start()
        print(f"[FileWatcherService] {self.filepath} 감시 시작")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print(f"[FileWatcherService] 감시 종료")
