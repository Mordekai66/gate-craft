"""Render Boolean expressions as circuit images using Schemdraw."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

from schemdraw.parsing import logicparse


def render_circuit(expression, output_path, dpi=200):
    """
    Render a logic expression and save it as a PNG image.

    Args:
        expression: Boolean expression in Schemdraw parser syntax.
        output_path: Destination path for the image.
        dpi: Image resolution.

    Returns:
        Path: Path to the generated image.

    Raises:
        RuntimeError: If circuit rendering fails.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        drawing = logicparse(expression, gateH=1.4, gateW=2.0, outlabel="Y")

        drawing.save(str(output_path), dpi=dpi)

    except Exception as error:
        raise RuntimeError(
            f"Could not render circuit.\n"
            f"Expression: {expression}\n"
            f"Output: {output_path}"
        ) from error

    return output_path