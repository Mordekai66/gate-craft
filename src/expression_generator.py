"""Generate random Boolean expressions and convert them to different formats."""

import random

OPERATORS = ["AND", "OR", "XOR", "NAND", "NOR", "XNOR"]

def generate_tree(variables):
    """Generate a random Boolean expression tree."""

    variables = variables.copy()
    random.shuffle(variables)

    def build(items):
        if len(items) == 1:
            node = ("INPUT", items[0])

            if random.random() < 0.30:
                return ("NOT", (node,))

            return node

        split = random.randint(1, len(items) - 1)

        left = build(items[:split])
        right = build(items[split:])

        op = random.choice(OPERATORS)

        return (op, (left, right))

    return build(variables)


def to_parser_expression(node):
    """Convert the tree into a Schemdraw-compatible expression."""

    op, children = node

    if op == "INPUT":
        return children.lower()

    if op == "NOT":
        return f"(not {to_parser_expression(children[0])})"

    left = to_parser_expression(children[0])
    right = to_parser_expression(children[1])

    if op == "AND":
        return f"({left} and {right})"

    if op == "OR":
        return f"({left} or {right})"

    if op == "XOR":
        return f"({left} xor {right})"

    if op == "NAND":
        return f"(not ({left} and {right}))"

    if op == "NOR":
        return f"(not ({left} or {right}))"

    if op == "XNOR":
        return f"(not ({left} xor {right}))"

    raise ValueError(f"Unknown operator: {op}")


def to_answer(node):
    """Convert the tree into engineering Boolean notation."""

    op, children = node

    if op == "INPUT":
        return children

    if op == "NOT":
        return f"({to_answer(children[0])})'"

    left = to_answer(children[0])
    right = to_answer(children[1])

    if op == "AND":
        return f"({left} . {right})"

    if op == "OR":
        return f"({left} + {right})"

    if op == "XOR":
        return f"({left} XOR {right})"

    if op == "NAND":
        return f"({left} . {right})'"

    if op == "NOR":
        return f"({left} + {right})'"

    if op == "XNOR":
        return f"({left} XOR {right})'"

    raise ValueError(f"Unknown operator: {op}")
