from typing import Any
from typing import List

from src.COOL.token import Token


class Attribute(Token):
    def __init__(self, line: int) -> None:
        super().__init__(line)
