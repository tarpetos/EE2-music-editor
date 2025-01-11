import shutil
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path

import ffmpeg

from ..utils.funs import get_desired_thread_number
from .base_manager import Manager


class CompressManager(Manager):
    def execute(self) -> None:
        raise NotImplementedError


def get_ffmpeg_input(input_path: Path, output_path: Path) -> list[ffmpeg]:
    Path.mkdir(output_path, exist_ok=True)

    ffmpeg_cmds: list[ffmpeg] = []
    for file in Path(input_path).iterdir():
        if Path(file).suffix in (".mp3", ".m4a", ".aac", ".wav", ".ogg"):
            new_file_path: Path = Path(output_path, file.name)
            stream = ffmpeg.input(str(file)).output(str(new_file_path), ab="128k", ac=2, ar=44100, y=None)
            ffmpeg_cmds.append(stream)
    return ffmpeg_cmds


def start_ffmpeg_threads(ffmpeg_cmds: list[ffmpeg]) -> None:
    with ThreadPoolExecutor(max_workers=get_desired_thread_number(reserved=0)) as executor:
        executor.map(lambda stream: stream.run(), ffmpeg_cmds)


def main() -> None:
    _ffmpeg: str = "ffmpeg"
    if shutil.which(_ffmpeg) is None:
        raise RuntimeError(
            f"{_ffmpeg} is not installed! Install it using command:\n" f"\tsudo apt-get install {_ffmpeg}\n"
        )
    ffmpeg_cmds = get_ffmpeg_input(
        input_path=Path.home() / "EE2_bebra" / "Empire Earth II Gold Edition" / "music" / "Ambient",
        output_path=Path.home() / "EE2_bebra" / "Empire Earth II Gold Edition" / "music" / "Ambient" / "test",
    )
    start_ffmpeg_threads(ffmpeg_cmds)


if __name__ == "__main__":
    main()
