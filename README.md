# SmartConvert

SmartConvert is a Python desktop application for converting files through a
clean, approachable interface built with PySide6.

The first supported conversion is **PDF to Word**. Select or drop a PDF, choose
the PDF to Word card, and select an output folder. Conversion runs in the
background and creates a DOCX with the same base filename.

## Getting started

1. Create and activate a Python virtual environment.
2. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   python main.py
   ```

## Project structure

- `app/ui/` — user-interface components
- `app/converters/` — file-conversion implementations
- `app/services/` — application services
- `app/utils/` — shared utilities
- `assets/` — icons and images
- `output/` — generated files
- `temp/` — temporary working files
