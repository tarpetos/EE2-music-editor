from abc import ABC, abstractmethod


class BaseManager(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
