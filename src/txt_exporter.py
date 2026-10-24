"""Export a clean, informative plain-text answer key."""

from pathlib import Path
from collections import Counter
from datetime import datetime


def export_answers(questions, output_path="logic_questions/answers.txt", title="DIGITAL LOGIC - ANSWER KEY"):
    """Create a formatted answer key with study notes and statistics."""

    questions = list(questions)

    if not questions:
        raise ValueError("Cannot export an empty answer key.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = len(questions)
    input_counts = Counter()
    all_inputs = set()

    for question in questions:
        if "number" not in question or "answer" not in question:
            raise ValueError(
                "Each question must contain 'number' and 'answer'."
            )

        inputs = question.get("inputs", [])
        input_counts[len(inputs)] += 1
        all_inputs.update(inputs)

    separator = "=" * 68
    thin_line = "-" * 68

    lines = [
        separator,
        title.center(68),
        separator,
        "",
        "DOCUMENT INFORMATION",
        thin_line,
        f"Total questions       : {total}",
        f"Input variables       : {', '.join(sorted(all_inputs)) or 'N/A'}",
        f"Generated on          : {datetime.now():%Y-%m-%d %H:%M}",
        "Purpose               : Revision and self-assessment",
        "",
        "QUESTION DISTRIBUTION",
        thin_line,
    ]

    for count in sorted(input_counts):
        lines.append(
            f"Questions with {count} inputs : {input_counts[count]}"
        )

    lines.extend([
        "",
        "HOW TO USE THIS ANSWER KEY",
        thin_line,
        "1. Solve each circuit before checking its answer.",
        "2. Compare your expression with the listed answer.",
        "3. Pay attention to NOT operations and output inversions.",
        "4. Use the notation guide below when reviewing expressions.",
        "",
        "ANSWER KEY",
        separator,
    ])

    for index, question in enumerate(questions, start=1):
        number = question["number"]
        answer = str(question["answer"])
        inputs = question.get("inputs", [])
        expression = question.get("expression")

        lines.extend([
            "",
            f"QUESTION {number:02d}",
            thin_line,
            f"Inputs          : {', '.join(inputs) if inputs else 'N/A'}",
        ])

        if expression:
            lines.append(f"Circuit logic   : {expression}")

        lines.extend([
            "",
            "Final answer:",
            f"    Y = {answer}",
            "",
        ])

    lines.extend([
        separator,
        "BOOLEAN ALGEBRA - QUICK REFERENCE",
        separator,
        "",
        "BASIC OPERATORS",
        thin_line,
        "A . B     AND  : Output is 1 when both inputs are 1.",
        "A + B     OR   : Output is 1 when at least one input is 1.",
        "A'        NOT  : Inverts the value of A.",
        "(A . B)'  NAND : AND followed by NOT.",
        "(A + B)'  NOR  : OR followed by NOT.",
        "",
        "OTHER OPERATORS",
        thin_line,
        "A XOR B   XOR  : Output is 1 when inputs differ.",
        "(A XOR B)' XNOR: Output is 1 when inputs are equal.",
        "",
        "IMPORTANT NOTES",
        thin_line,
        "- Parentheses show which operation is performed first.",
        "- A prime symbol (') means inversion of the expression before it.",
        "- Follow the parentheses carefully when simplifying an expression.",
        "- The answer key gives the generated Boolean expression;",
        "  it does not automatically prove that the expression is simplified.",
        "",
        separator,
        "END OF ANSWER KEY".center(68),
        separator,
        "",
    ])

    with output_path.open("w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines))

    return output_path