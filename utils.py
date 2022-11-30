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
        minus_expr = Expression(expr.value - expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} - ({expr_2.expr})")
        risky_exprs.add(minus_expr)
        if expr_2.value != 0 and expr.value % expr_2.value == 0:
            div_expr = Expression(expr.value // expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} // ({expr_2.expr})")
            risky_exprs.add(div_expr)
    elif expr.value < expr_2.value:
        minus_expr = Expression(expr_2.value - expr.value, expr.used_digits + expr_2.used_digits, f"{expr_2.expr} - ({expr.expr})")
        risky_exprs.add(minus_expr)
        if expr.value != 0 and expr.value % expr_2.value == 0:
            div_expr = Expression(expr_2.value // expr.value, expr.used_digits + expr_2.used_digits, f"{expr_2.expr} // ({expr.expr})")
            risky_exprs.add(div_expr)
    else:
        minus_expr = Expression(0, expr.used_digits + expr_2.used_digits, f"{expr.expr} - ({expr_2.expr})")
        risky_exprs.add(minus_expr)
        div_expr = Expression(1, expr.used_digits + expr_2.used_digits, f"{expr.expr} // ({expr_2.expr})")
        if expr.value != 0:
            risky_exprs.add(div_expr)

    return {
        Expression(expr.value + expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} + ({expr_2.expr})"),
        Expression(expr.value * expr_2.value, expr.used_digits + expr_2.used_digits, f"{expr.expr} * ({expr_2.expr})"),
        *risky_exprs
    }


def contains_equivalent(exprs: Set[Expression], expr: Expression) -> bool:
    # Check if exprs contains an expression with the same value and used digits as expr
    return any(
        (e.value == expr.value and
        len(e.used_digits) == len(expr.used_digits) and
        all(d in expr.used_digits for d in e.used_digits))
        for e in exprs
        )

def disjoint_expressions(expr: Expression, exprs: Set[Expression]) -> Set[Expression]:
    return {e for e in exprs if not any(d in e.used_digits for d in expr.used_digits)}