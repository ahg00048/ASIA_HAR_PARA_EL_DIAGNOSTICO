from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidgetItem, QInputDialog,
    QGroupBox, QVBoxLayout, QTableWidget, QHeaderView
)
from PyQt6 import uic
from ui.config import *

class Widget_AlternativesTable(QWidget):
    """
    Widget que contiene, para cada criterio, una tabla de comparación por pares
    de las alternativas. Permite añadir/eliminar alternativas y renombrarlas.
    """
    def __init__(self, criteria_names):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "alternativesTable.ui", self)
        
        self.criteria_names = criteria_names  # lista de strings
        self.alternative_names = ["Alternativa 1", "Alternativa 2"]  # mínimo dos
        self._tables = []  # guardamos las QTableWidget creadas
        self._updating = False
        
        # Construir las tablas iniciales para cada criterio
        self._build_tables()
        
        # Conectar botones
        self.addAlternativeButton.clicked.connect(self.add_alternative)
        self.removeAlternativeButton.clicked.connect(self.remove_alternative)

    def _build_tables(self):
        """Crea un QGroupBox por cada criterio con su tabla correspondiente."""
        # Limpiar layout previo (por si se reconstruye)
        layout = self.criteriaContainer.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._tables.clear()
        
        for crit_name in self.criteria_names:
            group = QGroupBox(f"Criterio: {crit_name}")
            vbox = QVBoxLayout()
            table = self._create_alternative_table()
            vbox.addWidget(table)
            group.setLayout(vbox)
            layout.addWidget(group)
            self._tables.append(table)
        
        # Conectar señales de las tablas después de crearlas
        for table in self._tables:
            table.cellChanged.connect(self._on_cell_changed)
            table.horizontalHeader().sectionDoubleClicked.connect(self._edit_alternative_name)
            table.verticalHeader().sectionDoubleClicked.connect(self._edit_alternative_name)
    
    def _create_alternative_table(self):
        """Crea y configura una QTableWidget para comparar alternativas."""
        table = QTableWidget()
        n = len(self.alternative_names)
        table.setRowCount(n)
        table.setColumnCount(n)
        table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Cabeceras
        for i, name in enumerate(self.alternative_names):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(name))
            table.setVerticalHeaderItem(i, QTableWidgetItem(name))
        
        # Inicializar con 1 en todas las celdas
        self._updating = True
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem("1")
                table.setItem(i, j, item)
        self._updating = False
        
        # Hacer que las cabeceras sean clicables para renombrar
        table.horizontalHeader().setSectionsClickable(True)
        table.verticalHeader().setSectionsClickable(True)
        
        return table

    def add_alternative(self):
        """Añade una nueva alternativa a todas las tablas."""
        n = len(self.alternative_names)
        new_name = f"Alternativa {n + 1}"
        self.alternative_names.append(new_name)
        
        self._updating = True
        for table in self._tables:
            # Añadir fila y columna
            row = table.rowCount()
            table.setRowCount(row + 1)
            table.setColumnCount(row + 1)
            table.setHorizontalHeaderItem(row, QTableWidgetItem(new_name))
            table.setVerticalHeaderItem(row, QTableWidgetItem(new_name))
            
            # Rellenar nueva fila y columna con 1
            for i in range(row + 1):
                if i < row:
                    table.setItem(i, row, QTableWidgetItem("1"))
                table.setItem(row, i, QTableWidgetItem("1"))
            # Asegurar diagonal
            table.item(row, row).setText("1")
        self._updating = False

    def remove_alternative(self):
        """Elimina la última alternativa, manteniendo mínimo 2."""
        if len(self.alternative_names) <= 2:
            return
        self.alternative_names.pop()
        
        self._updating = True
        for table in self._tables:
            new_size = len(self.alternative_names)
            table.setRowCount(new_size)
            table.setColumnCount(new_size)
        self._updating = False

    def _edit_alternative_name(self, index):
        """Renombra una alternativa en todas las tablas."""
        current_name = self.alternative_names[index]
        new_name, ok = QInputDialog.getText(
            self, "Renombrar alternativa",
            f"Nuevo nombre para '{current_name}':",
            text=current_name
        )
        if ok and new_name.strip():
            new_name = new_name.strip()
            self.alternative_names[index] = new_name
            # Actualizar cabeceras en todas las tablas
            self._updating = True
            for table in self._tables:
                table.horizontalHeaderItem(index).setText(new_name)
                table.verticalHeaderItem(index).setText(new_name)
            self._updating = False

    def _on_cell_changed(self, row, col):
        """Aplica reciprocidad en la tabla que emitió la señal."""
        if self._updating:
            return
        # Identificar qué tabla emitió (no es necesario un índice, usamos sender)
        table = self.sender()
        if not isinstance(table, QTableWidget):
            return
        item = table.item(row, col)
        if item is None:
            return
        
        try:
            text = item.text().strip()
            if '/' in text:
                val = float(eval(text))
            else:
                val = float(text)
        except (ValueError, SyntaxError):
            val = 1.0
        
        if val == 0:
            val = 1.0
        reciprocal = 1.0 / val
        
        # Representación amigable (fracción si es entero o 1/n)
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