import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from ui.widgets import widget_alternativesTable, widget_criteriaTable, widget_login, widget_patientsTable


# Ejemplo de uso integrado con CriteriaTable
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Supongamos que tenemos estos criterios (en una aplicación real vendrían del otro widget)
    criterios = ["Temperatura", "Costo", "Durabilidad"]
    
    alt_widget = widget_alternativesTable.Widget_AlternativesTable(criterios)
    alt_widget = widget_criteriaTable.Widget_CriteriaTable()
    alt_widget.show()
    sys.exit(app.exec())