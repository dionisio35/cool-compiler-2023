from abc import ABC
from abc import abstractmethod
from typing import Any


class Node(ABC):
    '''
    Base class for tokens.
    '''
    line: int
    column: int

    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.execute(*args, **kwds)

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def check(self):
        pass
