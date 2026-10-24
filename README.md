<div align="center">

# Gate Craft
### Boolean Circuit Worksheet Generator

Generate randomized digital-logic practice questions, render their logic-gate circuits, and export polished worksheets with or without answers.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Downloads](https://img.shields.io/github/downloads/Mordekai66/gate-craft/total?label=Downloads&logo=github)](https://github.com/Mordekai66/gate-craft/releases)
[![Repository Views](https://komarev.com/ghpvc/?username=Mordekai66&repo=gate-craft&label=Repository%20Views&color=blue)](https://github.com/Mordekai66/gate-craft)

</div>

---

## Overview

**Gate Craft** is a Python project for creating digital logic practice material. It builds Boolean-expression trees, validates their structure, renders the expressions as logic-circuit images, and exports the resulting questions into printable PDF worksheets and a separate text answer key.

It is designed for students who want repeatable practice with common Boolean operators and for educators who need generated circuit questions in a consistent format.

## Features

- 🎲 **Random question generation** — creates Boolean expressions using 2 or 3 input variables.
- 🔌 **Logic-gate coverage** — supports `AND`, `OR`, `NOT`, `XOR`, `NAND`, `NOR`, and `XNOR`.
- 🧩 **Expression validation** — checks tree structure, allowed operators and inputs, repeated variables, and input-count limits.
- 🖼️ **Circuit rendering** — renders expressions to PNG images using Schemdraw.
- 📄 **Two PDF editions** — exports a practice worksheet without answers and an answer edition.
- 🗝️ **Separate answer key** — writes a plain-text answer file with question details and a Boolean-algebra reference.
- 🧪 **Automated tests** — uses `pytest` to test generation, validation, and export behavior.
- 📁 **Organized output** — writes generated images and documents to the `output/` directory.

## Generated Files

Running the program creates the following files:

```text
output/
├── images/
│   ├── circuit_001.png
│   ├── circuit_002.png
│   └── ...
├── Logic_Questions_With_Answers.pdf
├── Logic_Questions_Practice.pdf
└── answers.txt
```

The default configuration generates **14 questions**. Each run creates a new randomized set of questions and overwrites output files with the same names.

## Requirements

- Python 3.10 or newer
- The Python packages listed in [`requirements.txt`](requirements.txt)

## Installation

1. Clone the repository:

2. Open the project directory:

   ```bash
   cd gate-craft
   ```

3. (Recommended) Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

Run the generator from the repository root—the directory containing `main.py`:

```bash
python main.py
```

Generated circuit images, PDFs, and the answer key will be saved under `output/`.

The default settings are defined near the top of `main.py`:

```python
NUM_QUESTIONS = 14
MIN_INPUTS = 2
MAX_INPUTS = 3
```

You can adjust these values to change the number of questions and the supported input range. The generator currently supports 2–3 inputs and a maximum of 100 questions per run.

## Project Structure

```text
gate-craft/
├── output/                       # Generated images and documents
├── src/
│   ├── circuit_renderer.py       # Render Boolean expressions as circuit images
│   ├── expression_generator.py   # Generate expression trees and output notation
│   ├── expression_validator.py   # Validate expression trees
│   ├── pdf_exporter.py           # Export PDF worksheets
│   ├── question_generator.py     # Build questions and render their circuits
│   └── txt_exporter.py           # Export the text answer key
├── tests/                        # Automated tests
│   ├── test_exporters.py
│   ├── test_expression_generator.py
│   ├── test_expression_validator.py
│   └── test_question_generator.py
├── .gitignore
├── LICENSE                       # MIT License
├── main.py                       # Main entry point
├── requirements.txt
└── README.md
```

## Boolean Operators

| Operator | Meaning | Output behavior |
|---|---|---|
| `AND` | Logical conjunction | 1 when both inputs are 1 |
| `OR` | Logical disjunction | 1 when at least one input is 1 |
| `NOT` | Logical inversion | Reverses the input value |
| `XOR` | Exclusive OR | 1 when the inputs differ |
| `NAND` | NOT-AND | Inverse of AND |
| `NOR` | NOT-OR | Inverse of OR |
| `XNOR` | Exclusive NOR | 1 when the inputs are equal |

## About the License


See the [`LICENSE`](LICENSE) file.
