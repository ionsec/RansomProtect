from typing import List

from modules.filesystem.canary import Canary
from modules.filesystem.monitor import FileSystemMonitor

if __name__ == "__main__":
    folders: List[str] = Canary.deploy()
    FileSystemMonitor.monitor(folders)
