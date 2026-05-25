import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from ui.widgets import widget_alternativesTable, widget_criteriaTable, widget_login, widget_patientsTable
from ui.main_window import Main_window

# Ejemplo de uso integrado con CriteriaTable
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_window()
    window.go_to_criteriaTable()
    window.show()
    # Supongamos que tenemos estos criterios (en una aplicación real vendrían del otro widget)
    
    sys.exit(app.exec())