"""Coordinate question generation, validation, and circuit rendering."""

import random
from pathlib import Path

from src.expression_generator import generate_tree, to_parser_expression, to_answer
from src.expression_validator import validate_tree
from src.circuit_renderer import render_circuit

def generate_questions(count=20, min_inputs=2, max_inputs=3, image_dir="logic_questions/images"):
    """
    Generate logic questions and render each circuit to a PNG.

    Args:
        count: Number of questions to generate.
        min_inputs: Minimum number of inputs per question.
        max_inputs: Maximum number of inputs per question.
        image_dir: Folder where circuit PNG files are saved.

    Returns:
        A list of question dictionaries ready for PDF export.

    Each question dictionary contains:
        number, inputs, expression, answer, image
    """
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer.")

    if min_inputs < 2 or max_inputs > 3 or min_inputs > max_inputs:
        raise ValueError("This version supports min_inputs/max_inputs between 2 and 3.")
    
    if count > 100:
        raise ValueError("This version supports a maximum of 100 questions.")

    image_dir = Path(image_dir)
    image_dir.mkdir(parents=True, exist_ok=True)

    questions = []

    for number in range(1, count + 1):
        input_count = random.randint(min_inputs, max_inputs)
        variables = list("ABC"[:input_count])

        # 1. Generate the Boolean expression tree.
        tree = generate_tree(variables)

        # 2. Validate the tree before using it.
        validate_tree(tree, allowed_inputs=variables, min_inputs=min_inputs, max_inputs=max_inputs)

        # 3. Convert the tree to the renderer syntax and answer notation.
        expression = to_parser_expression(tree)
        answer = to_answer(tree)

        # 4. Render one image for this question.
        image_path = image_dir / f"circuit_{number:03}.png"
        try:
            render_circuit(expression=expression, output_path=image_path, dpi=200)
        except Exception as error:
            raise RuntimeError(
                f"Failed to generate question {number}. "
                f"Expression: {expression}"
            ) from error

        # Append each question exactly once.
        questions.append(
            {
                "number": number,
                "inputs": variables,
                "expression": expression,
                "answer": answer,
                "image": image_path,
            }
        )

    return questions
