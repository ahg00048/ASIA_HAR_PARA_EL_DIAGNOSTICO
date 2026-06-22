from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QInputDialog
from PyQt6.QtCore import Qt, QEvent
from PyQt6 import uic

from ui.config import RESOURCES_DIR
from core.criteria import Criteria, relateCriterias, alterCriteriasWeight, unrelateCriterias


class CriteriaTable(QWidget):
    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "criteriaTable.ui", self)

        self._model = model  # instancia de Crit_Alt
        self._updating = False

        # Construir la tabla inicial desde el modelo
        self._build_table()

        # Conexión de botones
        self.addCriterionButton.clicked.connect(self.add_criterion)
        self.removeCriterionButton.clicked.connect(self.remove_criterion)

        self._callback_nextButton = callback_nextButton
        self._callback_backButton = callback_backButton

        self.saveButton.clicked.connect(self.criteria_save_current_config)
        self.backButton.clicked.connect(self.button_wrapper_backButton)
        self.nextButton.clicked.connect(self.button_wrapper_nextButton)

        # Reciprocidad al editar celdas
        self.tableWidget.cellChanged.connect(self._on_cell_changed)

        # Edición de nombres mediante doble clic en cabeceras
        self.tableWidget.horizontalHeader().setSectionsClickable(True)
        self.tableWidget.verticalHeader().setSectionsClickable(True)
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.edit_criterion_name)
        self.tableWidget.verticalHeader().sectionDoubleClicked.connect(self.edit_criterion_name)
    
        self.nextButton.installEventFilter(self)
        self.backButton.installEventFilter(self)

    # ------------------------------------------------------------------
    # Filtro de eventos para cambiar tooltip según condición en hover
    # ------------------------------------------------------------------
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ToolTip:
            if obj == self.nextButton:
                # Condición: si los datos no están listos y hay carga en curso
                if self._model.errorObtainingDFs():
                    self.nextButton.setToolTip("Error de conexión. Inténtelo de nuevo más tarde.")
                elif self._model.getDataframes() is None:
                    self.nextButton.setToolTip("Espere mientras se obtienen los datos…")
                else:
                    self.nextButton.setToolTip("Avanzar a la siguiente vista")
                return False  # ya manejamos el evento

        return super().eventFilter(obj, event)

    # ------------------------------------------------------------------
    # Construcción / reconstrucción de la tabla desde el modelo
    # ------------------------------------------------------------------
    def _build_table(self):
        criteria = list(self._model.getCriteria())
        n = len(criteria)
        table = self.tableWidget

        self._updating = True
        table.setRowCount(n)
        table.setColumnCount(n)

        for i, crit_i in enumerate(criteria):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(crit_i.name))
            table.setVerticalHeaderItem(i, QTableWidgetItem(crit_i.name))
            for j, crit_j in enumerate(criteria):
                weight = crit_i.getCritWeight_Crit(crit_j)
                if weight is None:
                    # Crear la relación si falta (para robustez)
                    relateCriterias(crit_i, crit_j, 1.0)
                    weight = 1.0
                item = QTableWidgetItem(self._format_ahp_weight(weight))
                # Bloquear edición en la diagonal
                if i == j:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(i, j, item)
        self._updating = False

    def _rebuild_table(self):
        self._build_table()

    @staticmethod
    def _format_ahp_weight(weight):
        """Convierte un peso numérico en una cadena amigable para AHP."""
        if weight == int(weight):
            return str(int(weight))
        n_val = round(1.0 / weight) if weight != 0 else 1
        if abs(weight - 1.0 / n_val) < 1e-9 and 1 <= n_val <= 9:
            return f"1/{n_val}"
        return f"{weight:.3g}"

    # ------------------------------------------------------------------
    # Operaciones sobre criterios (añadir, eliminar, renombrar)
    # ------------------------------------------------------------------
    def add_criterion(self):
        """Añade un nuevo criterio al modelo y reconstruye la tabla."""
        criteria = list(self._model.getCriteria())
        n = len(criteria)
        new_crit = Criteria(f"Criterio {n + 1}")

        # Relaciones consigo mismo y con los demás criterios (peso 1)
        new_crit.addCriteriaRel_Self()
        for crit in criteria:
            relateCriterias(new_crit, crit, 1.0)

        criteria.append(new_crit)
        self._model.updateCriteria(criteria)
        self._rebuild_table()

    def remove_criterion(self):
        """Elimina el último criterio (mínimo 2)."""
        criteria = list(self._model.getCriteria())
        if len(criteria) <= 2:
            return

        crit_to_remove = criteria[-1]
        # Quitar todas las relaciones que impliquen a este criterio
        for crit in criteria:
            if crit != crit_to_remove:
                unrelateCriterias(crit_to_remove, crit)

        criteria.remove(crit_to_remove)
        self._model.updateCriteria(criteria)
        self._rebuild_table()

    def edit_criterion_name(self, index):
        """Renombra un criterio en el modelo y en las cabeceras."""
        criteria = list(self._model.getCriteria())
        if index >= len(criteria):
            return

        crit = criteria[index]
        current_name = crit.name
        new_name, ok = QInputDialog.getText(
            self, "Renombrar criterio",
            f"Nuevo nombre para '{current_name}':",
            text=current_name
        )
        if ok and new_name.strip():
            new_name = new_name.strip()
            crit.name = new_name

            # Actualizar cabeceras horizontal y vertical
            self._updating = True
            self.tableWidget.horizontalHeaderItem(index).setText(new_name)
            self.tableWidget.verticalHeaderItem(index).setText(new_name)
            self._updating = False

            # Persistir (la lista ya está modificada)
            self._model.updateCriteria(criteria)

    # ------------------------------------------------------------------
    # Reciprocidad automática usando el modelo
    # ------------------------------------------------------------------
    def _on_cell_changed(self, row, col):
        if self._updating:
            return
        # Si se intenta editar la diagonal, revertir y salir
        if row == col:
            self._updating = True
            self.tableWidget.item(row, col).setText("1")
            self._updating = False
            return

        table = self.tableWidget
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

        criteria = list(self._model.getCriteria())
        crit_row = criteria[row]
        crit_col = criteria[col]

        # Actualizar el modelo (esto fija ambas direcciones)
        alterCriteriasWeight(crit_row, crit_col, val)

        # Leer los pesos actualizados y mostrarlos en ambas celdas
        self._updating = True
        w_row_col = crit_row.getCritWeight_Crit(crit_col)
        w_col_row = crit_col.getCritWeight_Crit(crit_row)

        table.item(row, col).setText(self._format_ahp_weight(w_row_col))
        table.item(col, row).setText(self._format_ahp_weight(w_col_row))
        self._updating = False


    def criteria_save_current_config(self):
        self._model.saveCriteria()


    def button_wrapper_nextButton(self):
        if self._model.getDataframes() is None:
            return
        
        self._callback_nextButton()
        

    def button_wrapper_backButton(self):
        self._model.cancelDataframes()        
        self._callback_backButton()