"""Main SmartConvert dashboard window."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QScrollArea, QSizePolicy, QVBoxLayout, QWidget,
)

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
        upload = UploadWidget()
        shadow = QGraphicsDropShadowEffect(upload)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 105))
        upload.setGraphicsEffect(shadow)
        self.content_layout.addWidget(upload)
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
        status = QLabel("READY")
        status.setObjectName("StatusBadge")
        status_row.addWidget(title)
        status_row.addStretch()
        status_row.addWidget(status)
        message = QLabel("Select a file and conversion type to begin")
        message.setObjectName("EmptyText")
        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        progress_layout.addLayout(status_row)
        progress_layout.addWidget(message)
        progress_layout.addSpacing(5)
        progress_layout.addWidget(progress)

        recent_card = QFrame()
        recent_card.setObjectName("BottomCard")
        recent_layout = QHBoxLayout(recent_card)
        recent_layout.setContentsMargins(20, 17, 20, 17)
        recent_icon = QLabel("◷")
        recent_icon.setObjectName("EmptyIcon")
        recent_copy = QVBoxLayout()
        recent_title = QLabel("Recent conversions")
        recent_title.setObjectName("SectionTitle")
        recent_empty = QLabel("Your converted files will appear here")
        recent_empty.setObjectName("EmptyText")
        recent_copy.addWidget(recent_title)
        recent_copy.addWidget(recent_empty)
        recent_layout.addWidget(recent_icon)
        recent_layout.addSpacing(7)
        recent_layout.addLayout(recent_copy)
        recent_layout.addStretch()
        grid.addWidget(progress_card, 0, 0)
        grid.addWidget(recent_card, 0, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        self.content_layout.addLayout(grid)
