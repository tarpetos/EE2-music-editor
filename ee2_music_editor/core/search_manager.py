import platform
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor

from ..utils.funs import get_desired_thread_number
from .base_manager import BaseManager


class SearchEngine:
    def __init__(self) -> None:
        self.platform_mapping = {
            "Windows": ...,
            "Linux": ...,
            "Darwin": ...,
        }


class SearchManager(BaseManager):
    def search(self, query: str) -> None:
        if platform.system() == "Windows":
            ...
        elif platform.system() == "Linux":
            ...
        elif platform.system() == "Darwin":
            ...
        else:
            raise NotImplementedError("Unsupported OS platform!")

        cmd = ["sudo", "plocate", query]
        # cmd = ["sudo", "find", "/", "-name", query]

        # cmd = ["sudo", "mdfind", "/", "-name", query]

        # cmd = f"gci -Path {drive} -Filter {filename} -Recurse
        # -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName"
        # cmd = ["powershell", "-Command", powershell_cmd]

        status = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = status.stdout.decode("utf-8")
        print(stdout)

    def execute(self) -> None:
        queries = ("EE2.exe", "EE2X.exe")
        with ThreadPoolExecutor(max_workers=get_desired_thread_number(len(queries))) as executor:
            executor.map(self.search, queries)
