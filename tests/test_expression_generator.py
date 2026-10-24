import pytest

from src.expression_generator import generate_tree, to_answer, to_parser_expression


def test_generate_tree_uses_each_variable_once():
    tree = generate_tree(["A", "B", "C"])

    def collect(node):
        operator, children = node
        if operator == "INPUT":
            return [children]
        if operator == "NOT":
            return collect(children[0])
        return collect(children[0]) + collect(children[1])

    assert sorted(collect(tree)) == ["A", "B", "C"]


def test_to_parser_expression_formats_input_and_not():
    assert to_parser_expression(("INPUT", "A")) == "a"
    assert to_parser_expression(("NOT", (("INPUT", "A"),))) == "(not a)"


def test_to_answer_formats_supported_operators():
    a = ("INPUT", "A")
    b = ("INPUT", "B")

    assert to_answer(("AND", (a, b))) == "(A . B)"
    assert to_answer(("OR", (a, b))) == "(A + B)"
    assert to_answer(("XOR", (a, b))) == "(A XOR B)"
    assert to_answer(("NAND", (a, b))) == "(A . B)'"
    assert to_answer(("NOR", (a, b))) == "(A + B)'"
    assert to_answer(("XNOR", (a, b))) == "(A XOR B)'"


def test_unknown_operator_raises_value_error():
    with pytest.raises(ValueError, match="Unknown operator"):
        to_answer(("INVALID", (("INPUT", "A"), ("INPUT", "B"))))
