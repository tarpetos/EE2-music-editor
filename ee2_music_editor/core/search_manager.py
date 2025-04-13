import platform
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor

from ee2_music_editor.utils.funs import get_desired_thread_number

from .manager import Manager


class SearchEngine:
    def __init__(self) -> None:
        self.platform_mapping = {
            "Windows": ...,
            "Linux": ...,
            "Darwin": ...,
        }


class SearchManager(Manager):
    def search(self, query: str) -> None:
        if platform.system() == "Windows" or platform.system() == "Linux" or platform.system() == "Darwin":
            ...
        else:
            msg = "Unsupported OS platform!"
            raise NotImplementedError(msg)

        cmd = ["sudo", "plocate", query]
        # cmd = ["sudo", "find", "/", "-name", query]

        # cmd = ["sudo", "mdfind", "/", "-name", query]

        # cmd = f"gci -Path {drive} -Filter {filename} -Recurse
        # -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName"
        # cmd = ["powershell", "-Command", powershell_cmd]

        status = subprocess.run(cmd, capture_output=True, check=False)
        status.stdout.decode("utf-8")

    def execute(self) -> None:
        queries = ("EE2.exe", "EE2X.exe")
        with ThreadPoolExecutor(max_workers=get_desired_thread_number(len(queries))) as executor:
            executor.map(self.search, queries)
