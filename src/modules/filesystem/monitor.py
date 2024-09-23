import shutil
import threading
import time
from pathlib import Path
from typing import Any, Dict, List

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from common.config.config import CONFIG
from common.log.splunk import Splunk
from modules.network.interface import NetworkInterface

from .canary import Canary

SENSITIVITY: Dict[str, int] = {
    "low": 3,
    "medium": 5,
    "high": 7,
}


class Countable:
    def __init__(self):
        self.fresh = True
        self.start()

    def start(self):
        _timer: int = CONFIG.getint("GENERAL", "TimeSensitivity")
        if _timer > 0:
            threading.Timer(_timer, self.update).start()

    def update(self):
        self.fresh = False


class Counter:
    def __init__(self, folder: str):
        self.folder: str = folder
        self.hits: int = 0
        self.events: Dict[str, Countable] = {}

        threading.Thread(target=self.start, daemon=True).start()

    def start(self):
        while True:
            time.sleep(1)
            self.count()

    def count(self):
        self.hits = sum(_.fresh == True for _ in self.events.values())

        if self.hits >= SENSITIVITY[CONFIG.get("GENERAL", "TrapSensitivity").lower()]:
            self.events = {}
            Splunk.alert(self.folder, self.hits)
            NetworkInterface.DROP()

    def insert(self, file: str):
        self.events[file] = Countable()


class FileSystemMonitor:
    COUNTERS: Dict[str, Any] = {}

    @staticmethod
    def monitor(folders: List[str]):
        observer = Observer()
        _handler = FileChangeHandler()

        for _dir in folders:
            FileSystemMonitor.COUNTERS[_dir] = Counter(_dir)
            observer.schedule(_handler, _dir, recursive=True)

        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            for _dir in folders:
                shutil.rmtree(_dir)

        observer.join()

    @staticmethod
    def handle(file: bytes | str):
        _path = Path(file)
        _dir = _path.parent
        _file = _path.name

        FileSystemMonitor.COUNTERS[str(_dir)].insert(_file)


class FileChangeHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        if Canary.is_decoy(event.src_path):
            if not event.is_directory:
                FileSystemMonitor.handle(event.src_path)

    def on_modified(self, event):
        if Canary.is_decoy(event.src_path):
            if not event.is_directory:
                with open(event.src_path, "r") as file:
                    content = file.read()
                    if not content == Canary.CONTENT:
                        FileSystemMonitor.handle(event.src_path)
                    else:
                        print("[DEBUG] TEST PASSED")

    def on_moved(self, event):
        if Canary.is_decoy(event.src_path) or Canary.is_decoy(event.dest_path):
            if not event.is_directory:
                FileSystemMonitor.handle(event.src_path)
