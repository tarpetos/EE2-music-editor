from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from typing import Final

from pydantic import dataclasses, field_validator


@dataclass
class _FilenameEnumerate:
    filename: str
    count: int
    start_from: int = 1

    def __new__(cls, filename: str, count: int, start_from: int = 1) -> list[str]:
        return [f"{filename}{value}" for value in range(start_from, start_from + count)]


@dataclasses.dataclass
class _FilenameExtender:
    extension: str = "mp3"
    filenames: list[str | _FilenameEnumerate] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.filenames = [
            f"{filename.removesuffix('.')}.{self.extension}" if not Path(filename).suffix else filename
            for filename in self.filenames
        ]

    @field_validator("extension")
    @classmethod
    def parse_extension(cls, value: str) -> str:
        return value.replace(".", "")


@dataclass
class ShellMusic(_FilenameExtender): ...


@dataclass
class RegionSet(_FilenameExtender):
    region: str | None = None


@dataclass
class EpochSet(_FilenameExtender):
    epoch_first: str | None = None
    epoch_last: str | None = None


@dataclass
class InGameMusic:
    region_sets: list[RegionSet]
    epoch_sets: list[EpochSet]


class EE2Music(Enum):
    SHELL: Final[ShellMusic] = ShellMusic(
        filenames=[
            "Shell_music",
            "Intro_movie_music",
        ]
    )
    IN_GAME: Final[InGameMusic] = InGameMusic(
        region_sets=[
            RegionSet(
                region="West",
                filenames=_FilenameEnumerate("amb_we_", count=10),
            ),
            RegionSet(
                region="FarEast",
                filenames=[
                    "amb_fe_1",
                    "amb_fe_2",
                    "amb_fe_3",
                    "amb_fe_4",
                    "amb_fe_4b" "amb_fe_5",
                    "amb_fe_5b",
                    "amb_fe_6",
                    "amb_fe_6b",
                    "amb_fe_6c",
                    "amb_fe_7",
                    "amb_fe_8",
                    "amb_fe_9",
                    "amb_fe_10",
                    "amb_fe_11",
                ],
            ),
            RegionSet(
                region="MiddleEast",
                filenames=[
                    "amb_me_1",
                    "amb_me_1b",
                    "amb_me_2",
                    "amb_me_2b",
                    "amb_me_2c",
                    "amb_me_2d",
                    "amb_me_2e",
                    "amb_me_3",
                    "amb_me_4",
                    "amb_me_5",
                    "amb_me_6",
                    "amb_me_7",
                    "amb_me_8",
                    "amb_me_9",
                    "amb_me_10",
                    "amb_me_11",
                    "amb_me_11b",
                    "amb_me_11c",
                    "amb_me_12",
                    "amb_me_13",
                ],
            ),
            RegionSet(
                region="MesoAmerican",
                filenames=[
                    "amb_am_1",
                    "amb_am_1b",
                    "amb_am_1c",
                    "amb_am_1d",
                    "amb_am_1e",
                    "amb_am_2",
                    "amb_am_2b",
                    "amb_am_2c",
                    "amb_am_2d",
                    "amb_am_3",
                    "amb_am_4",
                    "amb_am_5",
                    "amb_am_6",
                    "amb_am_7",
                    "amb_am_8",
                ],
            ),
            # @EE2X @MRC
            # New African region music.
            RegionSet(
                region="African",
                filenames=_FilenameEnumerate("amb_af_", count=13),
            ),
        ],
        epoch_sets=[
            # 1-10
            EpochSet(
                epoch_first="Stone",
                epoch_last="Industrial",
            ),
            # 11-13
            EpochSet(
                epoch_first="Modern",
                epoch_last="Digital",
                filenames=_FilenameEnumerate("amb_mid_late_", count=8),
            ),
            # 14-15
            EpochSet(
                epoch_first="Genetic",
                epoch_last="Synthetic",
                filenames=_FilenameEnumerate("amb_mid_late_", count=8),
            ),
        ],
    )


class Epoch(IntEnum):
    STONE = 1
    COPPER = 2
    BRONZE = 3
    IRON = 4
    DARK = 5
    MIDDLE = 6
    RENAISSANCE = 7
    IMPERIAL = 8
    ENLIGHTENMENT = 9
    INDUSTRIAL = 10
    MODERN = 11
    ATOMIC = 12
    DIGITAL = 13
    GENETIC = 14
    SYNTHETIC = 15


print(EE2Music.SHELL)
print(EE2Music.IN_GAME)
