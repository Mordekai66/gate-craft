"""Generate circuit questions and export two PDF editions."""

import random
from pathlib import Path

from src.question_generator import generate_questions
from src.pdf_exporter import create_pdf
from src.txt_exporter import export_answers


# SETTINGS
NUM_QUESTIONS = 14
MIN_INPUTS = 2
MAX_INPUTS = 3

OUTPUT_DIR = Path("output")
IMAGE_DIR = OUTPUT_DIR / "images"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

random.seed()

# Generate one shared set of questions.
questions = generate_questions(
    count=NUM_QUESTIONS,
    min_inputs=MIN_INPUTS,
    max_inputs=MAX_INPUTS,
    image_dir=IMAGE_DIR,
)

# Version 1: answers included.
create_pdf(
    questions,
    OUTPUT_DIR / "Logic_Questions_With_Answers.pdf",
    include_answers=True,
    title="Digital Logic - Answer Edition",
)

# Version 2: no answers.
create_pdf(
    questions,
    OUTPUT_DIR / "Logic_Questions_Practice.pdf",
    include_answers=False,
    title="Digital Logic - Practice Worksheet",
)

# Optional separate answer key.
export_answers(
    questions,
    OUTPUT_DIR / "answers.txt",
)

print(f"Generated {len(questions)} questions.")
print("PDF with answers: logic_questions/Logic_Questions_With_Answers.pdf")
print("PDF without answers: logic_questions/Logic_Questions_Practice.pdf")
print("Separate key: logic_questions/answers.txt")