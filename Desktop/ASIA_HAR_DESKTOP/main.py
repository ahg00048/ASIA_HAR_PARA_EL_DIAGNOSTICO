import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from ui.widgets import widget_alternativesTable, widget_criteriaTable, widget_login, widget_patientsTable
from ui.main_window import Main_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_window()
    window.show()
    
    sys.exit(app.exec())