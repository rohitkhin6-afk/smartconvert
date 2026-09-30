"""Sidebar navigation for SmartConvert."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class Sidebar(QFrame):
    """Persistent primary application navigation."""

    NAV_ITEMS = (
        ("◆", "Dashboard"),
        ("▤", "PDF Tools"),
        ("▧", "Image Tools"),
        ("▥", "Office Tools"),
        ("◷", "History"),
        ("⚙", "Settings"),
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(232)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 22)
        layout.setSpacing(5)

        brand = QHBoxLayout()
        brand.setSpacing(11)
        mark = QLabel("S")
        mark.setObjectName("LogoMark")
        mark.setFixedSize(42, 42)
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        names = QVBoxLayout()
        names.setSpacing(0)
        title = QLabel("SmartConvert")
        title.setObjectName("LogoTitle")
        caption = QLabel("FILE CONVERTER")
        caption.setObjectName("LogoCaption")
        names.addWidget(title)
        names.addWidget(caption)
        brand.addWidget(mark)
        brand.addLayout(names)
        layout.addLayout(brand)
        layout.addSpacing(34)

        for index, (icon, text) in enumerate(self.NAV_ITEMS):
            button = QPushButton(f"{icon}    {text}")
            button.setObjectName("NavButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setProperty("active", index == 0)
            button.clicked.connect(lambda checked=False, selected=button: self._activate(selected))
            layout.addWidget(button)
            if text == "Office Tools":
                layout.addSpacing(13)

        layout.addStretch()
        footer = QLabel("SMARTCONVERT  •  v1.0\nPrivate, secure & reliable")
        footer.setObjectName("SidebarFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def _activate(self, selected: QPushButton) -> None:
        for button in self.findChildren(QPushButton, "NavButton"):
            button.setProperty("active", button is selected)
            button.style().unpolish(button)
            button.style().polish(button)
