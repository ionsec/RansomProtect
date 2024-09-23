import socket
import subprocess
from collections.abc import Iterator
from typing import Any, Dict, List

import psutil

from common.config.config import CONFIG


class NetworkInterface:
    @staticmethod
    def DROP():
        """_summary_"""
        if CONFIG.getbool("NETWORK", "Drop"):
            for interface in NetworkInterface.enumerate():
                NetworkInterface.disable(interface)

    @staticmethod
    def disable(interface: str):
        """_summary_

        Args:
            interface (str): _description_
        """
        try:
            subprocess.run(
                ["netsh", "interface", "set", "interface", interface, "disable"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"[-] Network interface '{interface}' disabled.")
        except subprocess.CalledProcessError:
            # TODO: Handle this error + Logger
            pass

    @staticmethod
    def enumerate() -> Iterator[str]:
        """_summary_

        Yields:
            Generator[str]: _description_
        """
        interfaces: Dict[str, List[Any]] = psutil.net_if_addrs()

        for interface, addresses in interfaces.items():
            for ipv4 in addresses:
                if NetworkInterface.valid(ipv4):
                    yield interface

    @staticmethod
    def valid(ipv4: Any) -> bool:
        """_summary_

        Args:
            ipv4 (Any): _description_

        Returns:
            bool: _description_
        """
        LOOPBACK = "127."

        if ipv4.family == socket.AF_INET and not ipv4.address.startswith(LOOPBACK):
            return True
        return False
