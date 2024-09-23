import ctypes
import os
import random
from os.path import join
from pathlib import Path, PurePath
from typing import List

from common.config.config import CONFIG

FILE_ATTRIBUTE_HIDDEN = 0x02


class Canary:
    PREFIX = CONFIG.get("GENERAL", "Prefix")
    CONTENT = "This is a decoy file created to detect ransomware activity."

    @staticmethod
    def deploy() -> List[str]:
        """_summary_"""
        monitored: List[str] = []

        for _dir in Canary.paths():
            folder: str = join(_dir, NameGenerator.generate())

            Path(folder).mkdir(parents=True, exist_ok=True)
            Canary.hide(folder)
            monitored.append(folder)

            for _ext in CONFIG.getlist("GENERAL", "Extensions"):
                Canary.create_file(folder, _ext)

        return monitored

    @staticmethod
    def create_file(folder: str, extension: str):
        """_summary_

        Args:
            folder (str): _description_
            extension (str): _description_
        """
        _file = join(folder, NameGenerator.generate(extension))

        if os.path.exists(_file):
            # TODO: Handle this error + Logger
            return

        with open(_file, "w") as file:
            file.write(Canary.CONTENT)

        Canary.hide(_file)

    @staticmethod
    def hide(path: str):
        """_summary_

        Args:
            path (str): _description_
        """
        try:
            if not ctypes.windll.kernel32.SetFileAttributesW(
                str(path), FILE_ATTRIBUTE_HIDDEN
            ):
                raise ctypes.WinError()
        except OSError:
            # TODO: Handle this error + Logger
            pass

    @staticmethod
    def paths() -> List[str]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        relative: List[str] = CONFIG.getlist("GENERAL", "Paths")
        absolute: List[str] = []

        for _dir in relative:
            if _dir.startswith("C:/"):
                absolute.append(_dir)
            else:
                absolute.append(join(join(os.environ["USERPROFILE"]), _dir))

        return absolute

    @staticmethod
    def is_decoy(file: str) -> bool:
        """_summary_

        Args:
            file (str): _description_

        Returns:
            bool: _description_
        """
        _file = Path(file)

        try:
            if not _file.name.startswith(Canary.PREFIX):
                return False

            if not _file.suffix in CONFIG.getlist("GENERAL", "Extensions"):
                return False
        except PermissionError:
            return False

        return True


class NameGenerator:
    DICTIONARY = [
        "important",
        "confidential",
        "report",
        "backup",
        "financial",
        "data",
        "presentation",
        "security",
        "project",
        "plan",
        "analysis",
    ]

    @staticmethod
    def generate(extension: str = "") -> str:
        """Generate a random name

        Args:
            extension (str, optional): file extension. Defaults to "".

        Returns:
            str: random file/folder name
        """
        size: int = random.randint(2, 4)
        parts: List[str] = random.sample(NameGenerator.DICTIONARY, size)
        name: str = "_".join(parts)

        return Canary.PREFIX + name + extension
