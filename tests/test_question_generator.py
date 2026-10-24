import pytest

pytest.importorskip("schemdraw", reason="Schemdraw is required for circuit generation tests")
from src.question_generator import generate_questions


def test_rejects_non_positive_count(tmp_path):
    with pytest.raises(ValueError, match="count must be a positive integer"):
        generate_questions(count=0, image_dir=tmp_path / "images")


def test_rejects_more_than_three_inputs(tmp_path):
    with pytest.raises(ValueError, match="supports min_inputs/max_inputs"):
        generate_questions(count=1, min_inputs=2, max_inputs=4, image_dir=tmp_path / "images")


def test_rejects_more_than_one_hundred_questions(tmp_path):
    with pytest.raises(ValueError, match="maximum of 100"):
        generate_questions(count=101, image_dir=tmp_path / "images")


def test_generates_questions_and_circuit_images(tmp_path):
    questions = generate_questions(count=2, min_inputs=2, max_inputs=2, image_dir=tmp_path / "images")

    assert len(questions) == 2
    for number, question in enumerate(questions, start=1):
        assert question["number"] == number
        assert question["inputs"] and len(question["inputs"]) == 2
        assert question["expression"]
        assert question["answer"]
        assert question["image"].is_file()
