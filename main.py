"""Application entry point for SmartConvert."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650


def create_main_window() -> QMainWindow:
    """Create and configure the main SmartConvert window."""
    window = QMainWindow()
    window.setWindowTitle("SmartConvert")
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    welcome_label = QLabel("Welcome to SmartConvert")
    welcome_label.setStyleSheet("font-size: 24px;")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(welcome_label)

    return window


def main() -> int:
    """Run the SmartConvert desktop application."""
    application = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
