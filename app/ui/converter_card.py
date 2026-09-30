"""Reusable conversion shortcut card."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class ConverterCard(QFrame):
    """A styled, reusable conversion option."""

    selected = Signal(str)

    def __init__(self, icon: str, title: str, description: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ConverterCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(105)
        self.title = title

        layout = QHBoxLayout(self)
        layout.setContentsMargins(17, 16, 15, 16)
        layout.setSpacing(13)
        icon_label = QLabel(icon)
        icon_label.setObjectName("CardIcon")
        icon_label.setFixedSize(43, 43)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copy = QVBoxLayout()
        copy.setSpacing(4)
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        description_label = QLabel(description)
        description_label.setObjectName("CardDescription")
        description_label.setWordWrap(True)
        copy.addWidget(title_label)
        copy.addWidget(description_label)
        arrow = QLabel("›")
        arrow.setObjectName("Arrow")
        layout.addWidget(icon_label)
        layout.addLayout(copy, 1)
        layout.addWidget(arrow)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.rect().contains(event.position().toPoint())
        ):
            self.selected.emit(self.title)
        super().mouseReleaseEvent(event)
