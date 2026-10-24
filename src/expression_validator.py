"""Validate Boolean expression trees before rendering."""

ALLOWED_OPERATORS = {"INPUT", "NOT", "AND", "OR", "XOR", "NAND", "NOR", "XNOR"}

BINARY_OPERATORS = {"AND", "OR", "XOR", "NAND", "NOR", "XNOR"}

DEFAULT_INPUTS = {"A", "B", "C"}


def validate_tree(node, allowed_inputs=None, min_inputs=2, max_inputs=3):
    """
    Validate the structure of a Boolean expression tree.

    Returns:
        True if the tree is valid.

    Raises:
        ValueError if the tree is invalid.
    """

    if allowed_inputs is None:
        allowed_inputs = DEFAULT_INPUTS

    allowed_inputs = set(allowed_inputs)
    used_inputs = []

    def visit(current):
        # Every node must be a pair: (operator, children)
        if not isinstance(current, tuple) or len(current) != 2:
            raise ValueError(
                f"Invalid node structure: {current!r}"
            )

        operator, children = current

        if not isinstance(operator, str):
            raise ValueError("Operator must be a string.")

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(
                f"Unknown operator: {operator}"
            )

        # Input node
        if operator == "INPUT":
            if not isinstance(children, str):
                raise ValueError(
                    "INPUT node must contain a variable name."
                )

            if children not in allowed_inputs:
                raise ValueError(
                    f"Invalid input variable: {children}"
                )

            used_inputs.append(children)
            return

        # NOT has exactly one child
        if operator == "NOT":
            if not isinstance(children, tuple) or len(children) != 1:
                raise ValueError(
                    "NOT must have exactly one child."
                )

            visit(children[0])
            return

        # All other operators are binary
        if operator in BINARY_OPERATORS:
            if not isinstance(children, tuple) or len(children) != 2:
                raise ValueError(
                    f"{operator} must have exactly two children."
                )

            visit(children[0])
            visit(children[1])
            return

    visit(node)

    # Check for repeated input variables
    if len(used_inputs) != len(set(used_inputs)):
        raise ValueError(
            "Duplicate input variables found in the expression tree."
        )

    # Check the number of distinct inputs
    input_count = len(set(used_inputs))

    if not min_inputs <= input_count <= max_inputs:
        raise ValueError(
            f"Expected between {min_inputs} and {max_inputs} "
            f"inputs, but found {input_count}."
        )

    return True
