import json
import subprocess
import time

from common.config.config import CONFIG


class Splunk:
    @staticmethod
    def alert(folder: str, hits: int):
        _source = CONFIG.get("SPLUNK", "Source")
        _token = CONFIG.get("SPLUNK", "Token")
        _url = CONFIG.get("SPLUNK", "URL")

        _time = CONFIG.get("GENERAL", "TimeSensitivity")
        _count = CONFIG.get("GENERAL", "TrapSensitivity")

        log = f"time={int(time.time())}, interval={_time}, activity_treshold={_count}, event={hits} decoy files have benn manipulated in '{folder}'"
        data = {"sourcetype": _source, "event": log}
        command = [
            "curl",
            "-k",
            "-H",
            f"Authorization: Splunk {_token}",
            _url,
            "-d",
            json.dumps(data),
        ]

        try:
            print(f"[-] " + log)
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            # TODO: Handle this error + Logger
            pass
