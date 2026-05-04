import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.SetWindowTitle("window title")
        