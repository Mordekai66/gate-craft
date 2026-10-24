import pytest

from src.expression_validator import validate_tree


def test_valid_two_input_tree_returns_true():
    tree = ("AND", (("INPUT", "A"), ("NOT", (("INPUT", "B"),))))
    assert validate_tree(tree) is True


def test_rejects_unknown_operator():
    tree = ("BAD", (("INPUT", "A"), ("INPUT", "B")))
    with pytest.raises(ValueError, match="Unknown operator"):
        validate_tree(tree)


def test_rejects_duplicate_inputs():
    tree = ("OR", (("INPUT", "A"), ("INPUT", "A")))
    with pytest.raises(ValueError, match="Duplicate input"):
        validate_tree(tree)


def test_rejects_input_outside_allowed_set():
    tree = ("AND", (("INPUT", "A"), ("INPUT", "D")))
    with pytest.raises(ValueError, match="Invalid input variable"):
        validate_tree(tree)


def test_rejects_wrong_number_of_inputs():
    with pytest.raises(ValueError, match="Expected between"):
        validate_tree(("INPUT", "A"))


def test_rejects_invalid_not_arity():
    tree = ("NOT", (("INPUT", "A"), ("INPUT", "B")))
    with pytest.raises(ValueError, match="NOT must have exactly one child"):
        validate_tree(tree)
