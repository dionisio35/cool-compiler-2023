from typing import List

from COOL.nodes import Node
from COOL.semantic.visitor import Visitor_Class


class Method(Node):
    def __init__(self, line: int, column: int, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line, column)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor_Class):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: int, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.id = id
        super().__init__(line, column)

    def execute(self):
        raise NotImplementedError()

    def check(self,visitor: Visitor_Class):
        visitor.visit_execute_method(node = self)


class Attribute(Node):
    def __init__(self, line: int, column: int, id: str) -> None:
        self.id = id
        super().__init__(line, column)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor_Class):
        visitor.visit_attribute(self)

class AttributeDeclaration(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column, id)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor_Class):
        ...
        # visitor.visit_attribute_declaration(self)

class AttributeInicialization(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        super().__init__(line, column, id)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor_Class):
        visitor.visit_attribute_inicialization(self)

