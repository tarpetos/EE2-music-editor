from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum, auto
from pathlib import Path
from typing import Final

from pydantic import dataclasses


class Region(StrEnum):
    WEST = auto()
    FAR_EAST = auto()
    MIDDLE_EAST = auto()
    MESO_AMERICAN = auto()
    AFRICAN = auto()


class Epoch(IntEnum):
    STONE = auto()
    COPPER = auto()
    BRONZE = auto()
    IRON = auto()
    DARK = auto()
    MIDDLE = auto()
    RENAISSANCE = auto()
    IMPERIAL = auto()
    ENLIGHTENMENT = auto()
    INDUSTRIAL = auto()
    MODERN = auto()
    ATOMIC = auto()
    DIGITAL = auto()
    GENETIC = auto()
    SYNTHETIC = auto()


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
        self.extension = self.extension.replace(".", "")

        self.filenames = [
            f"{filename.removesuffix('.')}.{self.extension}" if not Path(filename).suffix else filename
            for filename in self.filenames
        ]


@dataclass
class ShellMusic(_FilenameExtender): ...


@dataclass
class RegionSet(_FilenameExtender):
    region: Region | None = None


@dataclass
class EpochSet(_FilenameExtender):
    epoch_first: Epoch | None = None
    epoch_last: Epoch | None = None


@dataclass
class InGameMusic:
    region_sets: list[RegionSet]
    epoch_sets: list[EpochSet]


# noinspection PyUnresolvedReferences
class EE2Music(Enum):
    EXPECTED_QUANTITY: Final[int] = 83  # 2 - shell music; 81 - in_game music

    SHELL: Final[ShellMusic] = ShellMusic(
        filenames=[
            "Shell_music",
            "Intro_movie_music",
        ]
    )

    IN_GAME: Final[InGameMusic] = InGameMusic(
        region_sets=[
            RegionSet(
                region=Region.WEST,
                filenames=_FilenameEnumerate("amb_we_", count=10),
            ),
            RegionSet(
                region=Region.FAR_EAST,
                filenames=[
                    "amb_fe_1",
                    "amb_fe_2",
                    "amb_fe_3",
                    "amb_fe_4",
                    "amb_fe_4b",
                    "amb_fe_5",
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
                region=Region.MIDDLE_EAST,
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
                region=Region.MESO_AMERICAN,
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
                region=Region.AFRICAN,
                filenames=_FilenameEnumerate("amb_af_", count=13),
            ),
        ],
        epoch_sets=[
            # 1-10
            EpochSet(
                epoch_first=Epoch.STONE,
                epoch_last=Epoch.INDUSTRIAL,
            ),
            # 11-13
            EpochSet(
                epoch_first=Epoch.MODERN,
                epoch_last=Epoch.DIGITAL,
                filenames=_FilenameEnumerate("amb_mid_late_", count=8),
            ),
            # 14-15
            EpochSet(
                epoch_first=Epoch.GENETIC,
                epoch_last=Epoch.SYNTHETIC,
                filenames=_FilenameEnumerate("amb_mid_late_", count=8),
            ),
        ],
    )

    @classmethod
    def by_shell(cls) -> list[str]:
        return cls.SHELL.value.filenames

    @classmethod
    def by_region(cls, region: Region | None = None) -> list[str]:
        return cls.__get_in_game_by_region(region)

    @classmethod
    def by_epoch(cls, epoch: Epoch | None = None) -> list[str]:
        return cls.__get_in_game_by_epoch(epoch)

    @classmethod
    def all(cls) -> list[str]:
        _all = cls.by_shell() + cls.by_region() + cls.by_epoch()
        assert (
            (actual_quantity := len(_all)) == cls.EXPECTED_QUANTITY.value
        ), f"Invalid number of MP3 files! Expected {cls.EXPECTED_QUANTITY.value}, got {actual_quantity}"
        return cls.by_shell() + cls.by_region() + cls.by_epoch()

    @classmethod
    def __get_in_game_by_region(cls, region: Region | None = None) -> list[str]:
        _lst = []

        if region is None:
            [_lst.extend(region_set.filenames) for region_set in cls.IN_GAME.value.region_sets]
        else:
            for region_set in cls.IN_GAME.value.region_sets:
                region_set.region == region and _lst.extend(region_set.filenames)

        return _lst

    @classmethod
    def __get_in_game_by_epoch(cls, epoch: Epoch | None = None) -> list[str]:
        _lst = []

        if epoch is None:
            [_lst.extend(epoch_set.filenames) for epoch_set in cls.IN_GAME.value.epoch_sets]
        else:
            for epoch_set in cls.IN_GAME.value.epoch_sets:
                epoch_set.epoch_first <= epoch <= epoch_set.epoch_last and _lst.extend(epoch_set.filenames)

        return list(dict.fromkeys(_lst))


print(EE2Music.by_shell())
print(EE2Music.by_region())
print(EE2Music.by_region(Region.WEST))
print(EE2Music.by_region(Region.AFRICAN))
print(EE2Music.by_epoch())
print(EE2Music.by_epoch(Epoch.STONE))
print(EE2Music.by_epoch(Epoch.MODERN))
print(EE2Music.all())
