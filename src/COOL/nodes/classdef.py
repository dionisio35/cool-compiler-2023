from typing import List

from COOL.semantic.visitor import Visitor
from COOL.nodes import Node
from COOL.nodes.feature import Method
from COOL.nodes.feature import Attribute


class Class(Node):
    def __init__(
        self,
        line: int,
        column: int,
        features: List[Method | Attribute],
        type: str,
        inherits: str = None
    ) -> None:
        self.type = type
        self.inherits = inherits
        self.features = features
        self.methods = [i for i in features if isinstance(i, Method)]
        self.attributes = [i for i in features if isinstance(i, Attribute)]
        self.inherits_instance: Class = None
        super().__init__(line,column)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        visitor.visit_class(self)

        for feature in self.features:
            feature.check(visitor)
