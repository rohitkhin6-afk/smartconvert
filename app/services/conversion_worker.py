"""Background conversion service used by the SmartConvert UI."""

from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from app.converters.pdf_to_word import convert_pdf_to_word


class ConversionWorker(QObject):
    """Perform one PDF conversion away from the GUI thread."""

    succeeded = Signal(str)
    failed = Signal(str)
    finished = Signal()

    def __init__(self, source: Path, output_folder: Path) -> None:
        super().__init__()
        self.source = source
        self.output_folder = output_folder

    @Slot()
    def run(self) -> None:
        try:
            output_path = convert_pdf_to_word(self.source, self.output_folder)
        except PermissionError:
            self.failed.emit(
                "File permission error. Check that the PDF and output folder are accessible."
            )
        except (ValueError, FileNotFoundError, NotADirectoryError) as error:
            self.failed.emit(str(error))
        except Exception as error:  # pdf2docx can surface several backend exceptions
            detail = str(error).strip()
            message = "Conversion failed. The PDF may be damaged or unsupported."
            if detail:
                message = f"{message}\n\nDetails: {detail}"
            self.failed.emit(message)
        finally:
            self.finished.emit()


class ConversionService(QObject):
    """Own worker threads and expose conversion results as Qt signals."""

    started = Signal()
    succeeded = Signal(str)
    failed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._threads: set[QThread] = set()
        self._workers: set[ConversionWorker] = set()

    def convert_pdf_to_word(self, source: str | Path, output_folder: str | Path) -> None:
        """Start a PDF-to-Word conversion without blocking the caller."""
        thread = QThread(self)
        worker = ConversionWorker(Path(source), Path(output_folder))
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.succeeded.connect(self.succeeded)
        worker.failed.connect(self.failed)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda current=thread: self._threads.discard(current))
        thread.finished.connect(lambda current=worker: self._workers.discard(current))

        self._threads.add(thread)
        self._workers.add(worker)
        self.started.emit()
        thread.start()
