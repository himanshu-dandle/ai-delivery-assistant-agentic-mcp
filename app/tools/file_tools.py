from pathlib import Path


def save_final_output_to_file(final_output: str, file_name: str = "final_delivery_output.md") -> str:
    """
    Save the final delivery output to a markdown file.
    Returns the saved file path.
    """

    output_dir = Path("data") / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / file_name

    file_path.write_text(final_output, encoding="utf-8")

    return str(file_path)