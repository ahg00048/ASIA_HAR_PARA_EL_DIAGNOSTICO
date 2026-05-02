import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton

app = QApplication(sys.argv)

window = QMainWindow()
window.show()  

app.exec()