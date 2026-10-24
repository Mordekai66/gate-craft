from PIL import Image
import pytest

from src.pdf_exporter import create_pdf
from src.txt_exporter import export_answers


def sample_question(image_path):
    Image.new("RGB", (240, 100), "white").save(image_path)
    return {
        "number": 1,
        "inputs": ["A", "B"],
        "expression": "(a and b)",
        "answer": "(A . B)",
        "image": image_path,
    }


def test_export_answers_writes_answer_key(tmp_path):
    output = tmp_path / "nested" / "answers.txt"
    result = export_answers([{
        "number": 1,
        "inputs": ["A", "B"],
        "expression": "(a and b)",
        "answer": "(A . B)",
    }], output)

    assert result == output
    content = output.read_text(encoding="utf-8")
    assert "Total questions       : 1" in content
    assert "(A . B)" in content


def test_export_answers_rejects_empty_list(tmp_path):
    with pytest.raises(ValueError, match="empty answer key"):
        export_answers([], tmp_path / "answers.txt")


def test_create_pdf_writes_pdf(tmp_path):
    image_path = tmp_path / "circuit.png"
    question = sample_question(image_path)
    output = tmp_path / "nested" / "questions.pdf"

    result = create_pdf([question], output, include_answers=True)

    assert result == output
    assert output.is_file()
    assert output.stat().st_size > 0
    assert output.read_bytes().startswith(b"%PDF")


def test_create_pdf_rejects_empty_questions(tmp_path):
    with pytest.raises(ValueError, match="At least one question"):
        create_pdf([], tmp_path / "empty.pdf")
