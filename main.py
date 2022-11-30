from utils import Expression, contains_result, get_possible_expressions, contains_equivalent, disjoint_expressions


def compute25(digits_str:str) -> str:
    digits = [int(d) for d in digits_str]
    valid_exprs = {Expression(d, [d], str(d)) for d in digits}
    unexplored_exprs = list(valid_exprs)
    while unexplored_exprs and not contains_result(valid_exprs):
        expr = unexplored_exprs.pop(0)
        new_valid_exprs = set()
        for expr_2 in disjoint_expressions(expr, valid_exprs):
            possible_exprs = get_possible_expressions(expr, expr_2)
            for possible_expr in possible_exprs:
                if not contains_equivalent(valid_exprs, possible_expr):
                    new_valid_exprs.add(possible_expr)
                    unexplored_exprs.append(possible_expr)
        valid_exprs.update(new_valid_exprs)

    if contains_result(valid_exprs):
        for e in valid_exprs:
            if e.value == 25 and len(e.used_digits) == 4:
                return e.expr
    else:
        return "SIN SOLUCIÓN"


if __name__ == "__main__":
    print(compute25("9871"))
