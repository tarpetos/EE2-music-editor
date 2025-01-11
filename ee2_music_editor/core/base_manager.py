from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
