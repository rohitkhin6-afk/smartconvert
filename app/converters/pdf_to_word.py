"""PDF to Word conversion implementation."""

from pathlib import Path

from pdf2docx import Converter


def convert_pdf_to_word(pdf_file: str | Path, output_folder: str | Path) -> Path:
    """Convert *pdf_file* to a same-named DOCX inside *output_folder*.

    Validation lives here as a second line of defence so callers other than the
    desktop UI receive useful exceptions too.
    """
    source = Path(pdf_file).expanduser()
    destination_folder = Path(output_folder).expanduser()

    if source.suffix.lower() != ".pdf":
        raise ValueError("The selected file must be a PDF.")
    if not source.is_file():
        raise FileNotFoundError("The selected PDF could not be found.")
    if not destination_folder.is_dir():
        raise NotADirectoryError("The selected output folder is invalid.")

    destination = destination_folder / f"{source.stem}.docx"
    converter = Converter(str(source))
    try:
        converter.convert(str(destination))
    finally:
        converter.close()

    if not destination.is_file():
        raise RuntimeError("The converter did not create an output file.")
    return destination
