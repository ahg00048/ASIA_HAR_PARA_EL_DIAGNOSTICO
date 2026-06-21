from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QInputDialog,
    QGroupBox, QVBoxLayout, QTableWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6 import uic
from ui.config import RESOURCES_DIR
from core.alternative import (
    Alternative, relateAlternatives, alterAlternativesWeight,
    unrelateAlternatives
)


class AlternativesTable(QWidget):
    """
    Widget que contiene, para cada criterio, una tabla de comparación por pares
    de las alternativas. Permite añadir/eliminar alternativas y renombrarlas.
    """

    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "alternativesTable.ui", self)

        self._model = model          # instancia de Crit_Alt
        self._updating = False
        self._tables = []           # lista de QTableWidget

        # Construir las tablas iniciales
        self._build_tables()

        # Conectar botones de la interfaz
        self.addAlternativeButton.clicked.connect(self.add_alternative)
        self.removeAlternativeButton.clicked.connect(self.remove_alternative)
        self.saveButton.clicked.connect(self.alternatives_save_current_config)
        self.backButton.clicked.connect(callback_backButton)
        self.nextButton.clicked.connect(callback_nextButton)

    # ----------------------------------------------------------------------
    # Construcción de la interfaz a partir del modelo
    # ----------------------------------------------------------------------
    def _build_tables(self):
        """Crea un QGroupBox por cada criterio con su tabla correspondiente."""
        layout = self.criteriaContainer.layout()
        # Limpiar layout previo
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._tables = []

        criteria = list(self._model.getCriteria())
        for crit in criteria:
            group = QGroupBox(f"Criterio: {crit.name}")
            vbox = QVBoxLayout()
            table = self._create_alternative_table(crit)
            vbox.addWidget(table)
            group.setLayout(vbox)
            layout.addWidget(group)
            self._tables.append(table)

        # Conectar señales después de crear todas las tablas
        for table in self._tables:
            table.cellChanged.connect(self._on_cell_changed)
            table.horizontalHeader().sectionDoubleClicked.connect(
                self._edit_alternative_name)
            table.verticalHeader().sectionDoubleClicked.connect(
                self._edit_alternative_name)

    def _create_alternative_table(self, crit):
        """Crea una QTableWidget para comparar alternativas según un criterio."""
        table = QTableWidget()
        alternatives = list(self._model.getAlternatives())
        n = len(alternatives)
        table.setRowCount(n)
        table.setColumnCount(n)
        table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.criterion = crit

        # Cabeceras
        for i, alt in enumerate(alternatives):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(alt.name))
            table.setVerticalHeaderItem(i, QTableWidgetItem(alt.name))

        self._updating = True
        for i, alt_i in enumerate(alternatives):
            for j, alt_j in enumerate(alternatives):
                weight = alt_i.getAltWeight_Crit_Alt(crit, alt_j)
                if weight is None:
                    relateAlternatives(crit, alt_i, alt_j, 1.0)
                    weight = 1.0
                item = QTableWidgetItem(self._format_ahp_weight(weight))
                # Bloquear edición en la diagonal
                if i == j:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(i, j, item)
        self._updating = False

        table.horizontalHeader().setSectionsClickable(True)
        table.verticalHeader().setSectionsClickable(True)
        return table

    def _rebuild_tables(self):
        """Reconstruye todas las tablas desde el modelo."""
        self._build_tables()

    @staticmethod
    def _format_ahp_weight(weight):
        """Formatea un peso numérico a su representación textual AHP."""
        # Corregido: comparar con int(weight), no float(weight)
        if weight == int(weight):
            return str(int(weight))
        n_val = round(1.0 / weight) if weight != 0 else 1
        if abs(weight - 1.0 / n_val) < 1e-9 and 1 <= n_val <= 9:
            return f"1/{n_val}"
        return f"{weight:.3g}"

    # ----------------------------------------------------------------------
    # Operaciones de modificación
    # ----------------------------------------------------------------------
    def add_alternative(self):
        """Añade una nueva alternativa al modelo y a la interfaz."""
        alternatives = list(self._model.getAlternatives())
        n = len(alternatives)
        new_alt = Alternative(f"Alternativa {n + 1}")

        criteria = list(self._model.getCriteria())

        # Relaciones consigo misma y con las existentes
        for crit in criteria:
            new_alt.addAlternativeRel_Self(crit)
            for alt in alternatives:
                relateAlternatives(crit, new_alt, alt, 1.0)

        alternatives.append(new_alt)
        self._model.updateAlternatives(alternatives)  # persistir

        # Reconstruir toda la interfaz
        self._rebuild_tables()

    def remove_alternative(self):
        """Elimina la última alternativa (mínimo 2)."""
        alternatives = list(self._model.getAlternatives())
        if len(alternatives) <= 2:
            return

        alt_to_remove = alternatives[-1]
        criteria = list(self._model.getCriteria())

        # Eliminar todas las relaciones que impliquen a esta alternativa
        for crit in criteria:
            for alt in alternatives:
                if alt != alt_to_remove:
                    unrelateAlternatives(crit, alt_to_remove, alt)

        alternatives.remove(alt_to_remove)
        self._model.updateAlternatives(alternatives)

        self._rebuild_tables()

    def _edit_alternative_name(self, index):
        """Renombra una alternativa en el modelo y en las cabeceras."""
        alternatives = list(self._model.getAlternatives())
        if index >= len(alternatives):
            return

        alt = alternatives[index]
        current_name = alt.name
        new_name, ok = QInputDialog.getText(
            self, "Renombrar alternativa",
            f"Nuevo nombre para '{current_name}':",
            text=current_name
        )
        if ok and new_name.strip():
            new_name = new_name.strip()
            alt.name = new_name

            self._updating = True
            for table in self._tables:
                table.horizontalHeaderItem(index).setText(new_name)
                table.verticalHeaderItem(index).setText(new_name)
            self._updating = False

            self._model.updateAlternatives(alternatives)

    def _on_cell_changed(self, row, col):
        """Actualiza el modelo cuando el usuario edita una celda y refleja la reciprocidad."""
        if self._updating:
            return

        # Seguridad extra para la diagonal (aunque no debería ser editable)
        if row == col:
            table = self.sender()
            if isinstance(table, QTableWidget):
                self._updating = True
                table.item(row, col).setText("1")
                self._updating = False
            return

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

        crit = table.criterion
        alternatives = list(self._model.getAlternatives())
        alt_row = alternatives[row]
        alt_col = alternatives[col]

        # Actualizar el modelo (esto fija ambas direcciones)
        alterAlternativesWeight(crit, alt_row, alt_col, val)

        # Refrescar las dos celdas desde el modelo para garantizar consistencia
        self._updating = True
        new_weight_row_col = alt_row.getAltWeight_Crit_Alt(crit, alt_col)
        new_weight_col_row = alt_col.getAltWeight_Crit_Alt(crit, alt_row)

        table.item(row, col).setText(self._format_ahp_weight(new_weight_row_col))
        table.item(col, row).setText(self._format_ahp_weight(new_weight_col_row))
        self._updating = False

    def alternatives_save_current_config(self):
        """Guarda explícitamente el estado actual de las alternativas."""
        self._model.saveAlternatives()