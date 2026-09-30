"""Main SmartConvert dashboard window."""

from pathlib import Path

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog, QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget,
)

from app.services.conversion_worker import ConversionService
from app.ui.converter_card import ConverterCard
from app.ui.sidebar import Sidebar
from app.ui.styles import APP_STYLE
from app.ui.upload_widget import UploadWidget


CONVERTERS = (
    ("W", "PDF to Word", "Turn PDFs into editable documents"),
    ("▧", "PDF to Image", "Export pages as sharp images"),
    ("P", "Image to PDF", "Create a PDF from any image"),
    ("P", "Word to PDF", "Create a polished PDF document"),
    ("P", "Excel to PDF", "Export spreadsheets with ease"),
    ("+", "Multiple Images to PDF", "Combine images into one PDF"),
)


class MainWindow(QMainWindow):
    """Responsive dashboard composing the modular SmartConvert UI."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SmartConvert — File Converter")
        self.setMinimumSize(900, 650)
        self.resize(1280, 820)
        self.setStyleSheet(APP_STYLE)
        self.selected_file: Path | None = None
        self.output_file: Path | None = None
        self.conversion_in_progress = False
        self.conversion_service = ConversionService(self)
        self.conversion_service.started.connect(self._conversion_started)
        self.conversion_service.succeeded.connect(self._conversion_succeeded)
        self.conversion_service.failed.connect(self._conversion_failed)

        root = QWidget()
        root.setObjectName("AppRoot")
        shell = QHBoxLayout(root)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)
        shell.addWidget(Sidebar())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("ScrollContent")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(40, 33, 40, 34)
        self.content_layout.setSpacing(24)
        self._build_header()
        self.upload = UploadWidget()
        self.upload.file_selected.connect(self._file_selected)
        shadow = QGraphicsDropShadowEffect(self.upload)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 105))
        self.upload.setGraphicsEffect(shadow)
        self.content_layout.addWidget(self.upload)
        self._build_converters()
        self._build_bottom()
        scroll.setWidget(content)
        shell.addWidget(scroll, 1)
        self.setCentralWidget(root)

    def _build_header(self) -> None:
        row = QHBoxLayout()
        copy = QVBoxLayout()
        copy.setSpacing(4)
        eyebrow = QLabel("SMART FILE CONVERSION")
        eyebrow.setObjectName("Eyebrow")
        heading = QLabel("Convert Your Files")
        heading.setObjectName("PageTitle")
        subtitle = QLabel("Fast, simple and secure file conversion")
        subtitle.setObjectName("PageSubtitle")
        copy.addWidget(eyebrow)
        copy.addWidget(heading)
        copy.addWidget(subtitle)
        secure = QLabel("●  Files stay private & secure")
        secure.setObjectName("SecurityPill")
        row.addLayout(copy)
        row.addStretch()
        row.addWidget(secure, alignment=Qt.AlignmentFlag.AlignTop)
        self.content_layout.addLayout(row)

    def _build_converters(self) -> None:
        heading = QHBoxLayout()
        title = QLabel("Popular conversions")
        title.setObjectName("SectionTitle")
        hint = QLabel("Choose a quick action to get started")
        hint.setObjectName("SectionHint")
        heading.addWidget(title)
        heading.addStretch()
        heading.addWidget(hint)
        self.content_layout.addLayout(heading)

        grid = QGridLayout()
        grid.setHorizontalSpacing(13)
        grid.setVerticalSpacing(13)
        for index, converter in enumerate(CONVERTERS):
            card = ConverterCard(*converter)
            card.selected.connect(self._converter_selected)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            grid.addWidget(card, index // 3, index % 3)
        self.content_layout.addLayout(grid)

    def _build_bottom(self) -> None:
        grid = QGridLayout()
        grid.setSpacing(13)

        progress_card = QFrame()
        progress_card.setObjectName("BottomCard")
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setContentsMargins(20, 17, 20, 18)
        status_row = QHBoxLayout()
        title = QLabel("Conversion progress")
        title.setObjectName("SectionTitle")
        self.status = QLabel("READY")
        self.status.setObjectName("StatusBadge")
        status_row.addWidget(title)
        status_row.addStretch()
        status_row.addWidget(self.status)
        self.progress_message = QLabel("Ready")
        self.progress_message.setObjectName("EmptyText")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        progress_layout.addLayout(status_row)
        progress_layout.addWidget(self.progress_message)
        progress_layout.addSpacing(5)
        progress_layout.addWidget(self.progress)

        recent_card = QFrame()
        recent_card.setObjectName("BottomCard")
        recent_layout = QHBoxLayout(recent_card)
        recent_layout.setContentsMargins(20, 17, 20, 17)
        recent_icon = QLabel("◷")
        recent_icon.setObjectName("EmptyIcon")
        recent_copy = QVBoxLayout()
        recent_title = QLabel("Conversion output")
        recent_title.setObjectName("SectionTitle")
        self.output_name = QLabel("No converted file yet")
        self.output_name.setObjectName("EmptyText")
        self.output_path = QLabel()
        self.output_path.setObjectName("OutputPath")
        self.output_path.setWordWrap(True)
        self.output_path.hide()
        recent_copy.addWidget(recent_title)
        recent_copy.addWidget(self.output_name)
        recent_copy.addWidget(self.output_path)
        actions = QHBoxLayout()
        self.open_file_button = QPushButton("Open File")
        self.open_folder_button = QPushButton("Open Folder")
        for button in (self.open_file_button, self.open_folder_button):
            button.setObjectName("ActionButton")
            button.hide()
            actions.addWidget(button)
        self.open_file_button.clicked.connect(self._open_output_file)
        self.open_folder_button.clicked.connect(self._open_output_folder)
        recent_copy.addLayout(actions)
        recent_layout.addWidget(recent_icon)
        recent_layout.addSpacing(7)
        recent_layout.addLayout(recent_copy)
        recent_layout.addStretch()
        grid.addWidget(progress_card, 0, 0)
        grid.addWidget(recent_card, 0, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        self.content_layout.addLayout(grid)

    def _file_selected(self, file_path: str) -> None:
        self.selected_file = Path(file_path)
        if not self.conversion_in_progress:
            self._show_ready()

    def _converter_selected(self, converter_name: str) -> None:
        if converter_name != "PDF to Word" or self.conversion_in_progress:
            return
        if self.selected_file is None:
            self._show_error("No file selected", "Select a PDF file before choosing PDF to Word.")
            return
        if self.selected_file.suffix.lower() != ".pdf":
            self._show_error("Wrong file type", "PDF to Word only accepts files with a .pdf extension.")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not output_folder:
            return
        folder = Path(output_folder)
        if not folder.is_dir():
            self._show_error("Invalid output folder", "Choose an existing output folder.")
            return
        self.conversion_service.convert_pdf_to_word(self.selected_file, folder)

    def _conversion_started(self) -> None:
        self.conversion_in_progress = True
        self.status.setText("CONVERTING")
        self.progress_message.setText("Converting PDF to Word...")
        self.progress.setRange(0, 0)

    def _conversion_succeeded(self, output_path: str) -> None:
        self.conversion_in_progress = False
        self.output_file = Path(output_path)
        self.status.setText("COMPLETED")
        self.progress_message.setText("Conversion completed successfully")
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.output_name.setText(self.output_file.name)
        self.output_path.setText(str(self.output_file.parent))
        self.output_path.show()
        self.open_file_button.show()
        self.open_folder_button.show()

    def _conversion_failed(self, message: str) -> None:
        self.conversion_in_progress = False
        self.status.setText("ERROR")
        self.progress_message.setText("Conversion failed")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self._show_error("Conversion failed", message)

    def _show_ready(self) -> None:
        self.status.setText("READY")
        self.progress_message.setText("Ready")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

    def _open_output_file(self) -> None:
        if self.output_file:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.output_file)))

    def _open_output_folder(self) -> None:
        if self.output_file:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.output_file.parent)))

    def _show_error(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)
