import json
import os
from configparser import ConfigParser
from typing import Any, List


class Config:
    _instance = None

    def __new__(cls, file: str = "config.ini") -> Any:
        """Create new instance

        Args:
            file (str, optional): path to configuration file. Defaults to "config.ini".

        Returns:
            Any: Config, a configuration descriptor
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize(file)

        return cls._instance

    def _initialize(self, file: str):
        """Init the new instance

        Args:
            file (str): path to configuration file.
        """
        self.file = file
        self.parser = ConfigParser()
        self.load()

    def load(self):
        """Load configuration file into Config instance

        Raises:
            FileNotFoundError: configuration file not found
        """
        if not os.path.exists(self.file):
            # TODO: Handle this error + Logger
            raise FileNotFoundError(f"Config file '{self.file}' not found.")

        self.parser.read(self.file)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        """Get option from section

        Args:
            section (str): configuration section
            option (str): option to retrieve
            fallback (Any, optional): fallback value. Defaults to None.

        Returns:
            Any: option value
        """
        return self.parser.get(section, option, fallback=fallback)

    def getint(self, section: str, option: str, fallback: int = None) -> int:
        """Get option from section

        Args:
            section (str): configuration section
            option (str): option to retrieve
            fallback (int, optional): fallback value. Defaults to None.

        Returns:
            int: option value
        """
        return self.parser.getint(section, option, fallback=fallback)

    def getfloat(self, section: str, option: str, fallback: float = None) -> float:
        """Get option from section

        Args:
            section (str): configuration section
            option (str): option to retrieve
            fallback (float, optional): fallback value. Defaults to None.

        Returns:
            float: option value
        """
        return self.parser.getfloat(section, option, fallback=fallback)

    def getbool(self, section: str, option: str, fallback: bool = None) -> bool:
        """Get option from section

        Args:
            section (str): configuration section
            option (str): option to retrieve
            fallback (bool, optional): fallback value. Defaults to None.

        Returns:
            bool: option value
        """
        return self.parser.getboolean(section, option, fallback=fallback)

    def getlist(self, section: str, option: str, fallback: List[str] = []) -> List[Any]:
        """Get option from section

        Args:
            section (str): configuration section
            option (str): option to retrieve
            fallback (List[str], optional): fallback value. Defaults to None.

        Returns:
            List[str]: option value
        """
        return json.loads(self.get(section, option, fallback=fallback))


CONFIG = Config()
