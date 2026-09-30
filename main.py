"""SmartConvert application entry point."""

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def main() -> int:
    """Launch the SmartConvert desktop application."""
    application = QApplication(sys.argv)
    application.setApplicationName("SmartConvert")
    application.setFont(QFont("Inter", 10))

    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
