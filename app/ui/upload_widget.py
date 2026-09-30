"""Drag-and-drop file selection widget."""

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class UploadWidget(QFrame):
    """File browser and drop target with inline validation feedback."""

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".jpg", ".jpeg", ".png"}
    file_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("UploadCard")
        self.setAcceptDrops(True)
        self.setMinimumHeight(285)
        self.selected_file: Path | None = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(32, 27, 32, 25)
        layout.setSpacing(9)

        self.icon = QLabel("⇧")
        self.icon.setObjectName("UploadIcon")
        self.icon.setFixedSize(60, 60)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = QLabel("Drag & Drop your file here")
        self.title.setObjectName("UploadTitle")
        self.detail = QLabel("or")
        self.detail.setObjectName("MutedText")
        self.file_meta = QLabel()
        self.file_meta.setObjectName("FileMeta")
        self.file_meta.hide()
        self.error = QLabel()
        self.error.setObjectName("ErrorLabel")
        self.error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error.hide()
        browse = QPushButton("Browse Files")
        browse.setObjectName("BrowseButton")
        browse.setCursor(Qt.CursorShape.PointingHandCursor)
        browse.clicked.connect(self.browse_files)

        layout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.detail, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.file_meta, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.error, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(browse, alignment=Qt.AlignmentFlag.AlignHCenter)

        formats = QHBoxLayout()
        formats.setSpacing(6)
        for extension in ("PDF", "DOCX", "XLSX", "JPG", "JPEG", "PNG"):
            chip = QLabel(extension)
            chip.setObjectName("FormatChip")
            formats.addWidget(chip)
        layout.addSpacing(4)
        layout.addLayout(formats)

    def browse_files(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a file",
            "",
            "Supported files (*.pdf *.docx *.xlsx *.jpg *.jpeg *.png);;All files (*)",
        )
        if file_path:
            self._select_file(Path(file_path))

    def _select_file(self, path: Path) -> None:
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            self.selected_file = None
            self.error.setText(f"{path.suffix.upper() or 'This file type'} is not supported. Choose a listed format.")
            self.error.show()
            return
        self.error.hide()
        self.selected_file = path
        self.icon.setText("✓")
        self.title.setText(path.name)
        self.title.setObjectName("FileName")
        self.title.style().unpolish(self.title)
        self.title.style().polish(self.title)
        size = path.stat().st_size if path.exists() else 0
        self.file_meta.setText(f"{self._format_size(size)}   •   {path.suffix[1:].upper()} file")
        self.file_meta.show()
        self.detail.setText("Ready to convert")
        self.file_selected.emit(str(path))

    @staticmethod
    def _format_size(byte_count: int) -> str:
        size = float(byte_count)
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024 or unit == "GB":
                return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
            size /= 1024
        return f"{size:.1f} GB"

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", True)
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event) -> None:  # noqa: N802
        self._clear_drag_state()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:  # noqa: N802
        self._clear_drag_state()
        local_files = [Path(url.toLocalFile()) for url in event.mimeData().urls() if url.isLocalFile()]
        if local_files:
            self._select_file(local_files[0])
            event.acceptProposedAction()

    def _clear_drag_state(self) -> None:
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
