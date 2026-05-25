from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QInputDialog
from PyQt6 import uic

from ui.config import *

class CriteriaTable(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "criteriaTable.ui", self)
        
        # Conexión de botones
        self.addCriterionButton.clicked.connect(self.add_criterion)
        self.removeCriterionButton.clicked.connect(self.remove_criterion)
        
        # Mantener reciprocidad al editar celdas
        self.tableWidget.cellChanged.connect(self.enforce_reciprocity)
        
        # Habilitar edición de nombres de criterio mediante doble clic en cabeceras
        self.tableWidget.horizontalHeader().setSectionsClickable(True)
        self.tableWidget.verticalHeader().setSectionsClickable(True)
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.edit_criterion_name)
        self.tableWidget.verticalHeader().sectionDoubleClicked.connect(self.edit_criterion_name)
        
        # Bloqueo para evitar recursividad en actualizaciones programáticas
        self._updating = False

    def add_criterion(self):
        """Añade una nueva fila y columna, con valor inicial 1 en toda la diagonal y extremos."""
        table = self.tableWidget
        n = table.rowCount()
        table.setRowCount(n + 1)
        table.setColumnCount(n + 1)
        
        # Nombre por defecto
        new_label = f"Criterio {n + 1}"
        table.setHorizontalHeaderItem(n, QTableWidgetItem(new_label))
        table.setVerticalHeaderItem(n, QTableWidgetItem(new_label))
        
        # Rellenar nueva fila y columna con 1 (excepto la diagonal, que ya se pone al crear)
        self._updating = True
        for i in range(n + 1):
            if i < n:
                # Celda en nueva columna (i, n)
                item_col = QTableWidgetItem("1")
                table.setItem(i, n, item_col)
            # Celda en nueva fila (n, i)
            item_row = QTableWidgetItem("1")
            table.setItem(n, i, item_row)
        # Aseguramos diagonal = 1
        table.item(n, n).setText("1")
        self._updating = False

    def remove_criterion(self):
        """Elimina la última fila y columna, manteniendo al menos 2 criterios."""
        table = self.tableWidget
        n = table.rowCount()
        if n <= 2:
            return
        table.setRowCount(n - 1)
        table.setColumnCount(n - 1)

    def enforce_reciprocity(self, row, col):
        """Actualiza la celda simétrica con el valor recíproco."""
        if self._updating:
            return
        table = self.tableWidget
        item = table.item(row, col)
        if item is None:
            return
        
        try:
            # Interpretar fracciones simples (como "1/3")
            text = item.text().strip()
            if '/' in text:
                val = float(eval(text))
            else:
                val = float(text)
        except (ValueError, SyntaxError):
            val = 1.0
        
        reciprocal = 1.0 / val if val != 0 else 1.0
        
        # Representación amigable (fracción 1/n si es exacta)
        if reciprocal == int(reciprocal):
            recip_text = str(int(reciprocal))
        else:
            n_val = round(1.0 / reciprocal) if reciprocal != 0 else 1
            if abs(reciprocal - 1.0/n_val) < 1e-9 and 1 <= n_val <= 9:
                recip_text = f"1/{n_val}"
            else:
                recip_text = f"{reciprocal:.3g}"
        
        self._updating = True
        sym_item = table.item(col, row)
        if sym_item is None:
            sym_item = QTableWidgetItem()
            table.setItem(col, row, sym_item)
        sym_item.setText(recip_text)
        self._updating = False

    def edit_criterion_name(self, index):
        """
        Abre un diálogo para cambiar el nombre del criterio en el índice dado.
        Se ejecuta al hacer doble clic en cualquier cabecera (horizontal o vertical).
        Actualiza ambas cabeceras para mantener la simetría.
        """
        table = self.tableWidget
        # Obtener el nombre actual desde la cabecera horizontal (o vertical, es simétrica)
        current_name = table.horizontalHeaderItem(index).text() if table.horizontalHeaderItem(index) else f"Criterio {index+1}"
        
        new_name, ok = QInputDialog.getText(
            self, "Renombrar criterio",
            f"Nuevo nombre para el criterio {index+1}:",
            text=current_name
        )
        
        if ok and new_name.strip():
            # Actualizar cabeceras horizontal y vertical
            table.horizontalHeaderItem(index).setText(new_name.strip())
            table.verticalHeaderItem(index).setText(new_name.strip())
