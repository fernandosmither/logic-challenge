from dataclasses import dataclass, field
from itertools import count
from typing import List, Set

@dataclass
class Expression:
    value: int = 0
    used_digits: List[int] = field(default_factory=list)
    expr: str = str(value)
    id: int = field(default_factory=count().__next__, init=False)

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: object) -> bool:
        return all(self.value == other.value,
                   len(self.used_digits) == len(other.used_digits),
                   all(d in other.used_digits for d in self.used_digits))


def contains_result(expressions: Set[Expression]) -> bool:
    return any((e.value == 25 and len(e.used_digits) == 4) for e in expressions)

def get_possible_expressions(expr: Expression, expr_2: Expression) -> Set[Expression]:
    risky_exprs = set()
    if expr.value > expr_2.value:
        minus_expr = Expression(expr.value - expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} - {expr_2.expr}")
        risky_exprs.add(minus_expr)
        if expr_2.value != 0 and expr.value % expr_2.value == 0:
            div_expr = Expression(expr.value // expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} // {expr_2.expr}")
            risky_exprs.add(div_expr)
    elif expr.value < expr_2.value:
        minus_expr = Expression(expr_2.value - expr.value, expr.used_digits + expr_2.used_digits, f"{expr_2.expr} - {expr.expr}")
        risky_exprs.add(minus_expr)
        if expr.value != 0 and expr.value % expr_2.value == 0:
            div_expr = Expression(expr_2.value // expr.value, expr.used_digits + expr_2.used_digits, f"{expr_2.expr} // {expr.expr}")
            risky_exprs.add(div_expr)
    else:
        minus_expr = Expression(0, expr.used_digits + expr_2.used_digits, f"{expr.expr} - {expr_2.expr}")
        risky_exprs.add(minus_expr)
        div_expr = Expression(1, expr.used_digits + expr_2.used_digits, f"{expr.expr} // {expr_2.expr}")
        if expr.value != 0:
            risky_exprs.add(div_expr)
    return {
        Expression(expr.value + expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} + {expr_2.expr}"),
        Expression(expr.value * expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} * {expr_2.expr}"),
        minus_expr,
        *risky_exprs
    }


def compute25(digits_str:str) -> str:
    digits = [int(d) for d in digits_str]
    valid_exprs = {Expression(d, [d], str(d)) for d in digits}
    unexplored_exprs = list(valid_exprs)
    while unexplored_exprs and not contains_result(valid_exprs):
        expr = unexplored_exprs.pop()
        for expr_2 in valid_exprs.copy():
            possible_exprs = get_possible_expressions(expr, expr_2)
            for possible_expr in possible_exprs:
                if possible_expr not in valid_exprs:
                    valid_exprs.add(possible_expr)
                    unexplored_exprs.append(possible_expr)

    # for e in valid_exprs:
    #     print(e)
    
    if contains_result(valid_exprs):
        for e in valid_exprs:
            if e.value == 25 and len(e.used_digits) == 4:
                return e
    else:
        return "SIN SOLUCIÓN"


if __name__ == "__main__":
    print(compute25("9871"))
