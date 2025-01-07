import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from mutagen.id3 import ID3, TXXX
from mutagen.mp3 import MP3


def add_metadata_to_file(file_path: str | Path, output_path: str | Path, metadata_string: str) -> None:
    audio = MP3(file_path, ID3=ID3)
    if audio.tags is None:
        audio.add_tags()
    audio.tags.add(TXXX(encoding=3, desc="EE2_MUSIC", text=metadata_string))

    shutil.copy(file_path, output_path)
    audio.save(output_path)


def decode_metadata_from_file(file_path: str | Path) -> dict[str, Any]:
    audio = MP3(file_path, ID3=ID3)
    if audio.tags is not None:
        for tag in audio.tags.values():
            if isinstance(tag, TXXX) and tag.desc == "EE2_MUSIC":
                return json.loads(tag.text[0])
        return {}


def main() -> None:
    current_date = datetime.now()
    metadata = {
        "year": current_date.year,
        "month": current_date.month,
        "day": current_date.day,
        "hour": current_date.hour,
        "minute": current_date.minute,
        "second": current_date.second,
    }
    metadata_string = json.dumps(metadata)

    input_path: Path = Path(__file__).absolute().parent / "music" / "init" / "amb_af_1.mp3"
    output_path: Path = Path(__file__).absolute().parent / "music" / "mutated" / "amb_af_1.mp3"

    add_metadata_to_file(input_path, output_path, metadata_string)
    result = decode_metadata_from_file(output_path)
    print(result)


if __name__ == "__main__":
    main()
