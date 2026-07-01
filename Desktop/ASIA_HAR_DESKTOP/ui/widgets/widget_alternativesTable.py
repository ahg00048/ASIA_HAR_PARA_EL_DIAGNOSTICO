from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QInputDialog,
    QGroupBox, QVBoxLayout, QTableWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6 import uic
from ui.config import RESOURCES_DIR
from core.ahp.alternative import (
    Alternative, relateAlternatives, alterAlternativesWeight,
    unrelateAlternatives
)
from core.fuzzy.fuzzyCriteria import FuzzyCriteria

class AlternativesTable(QWidget):
    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "alternativesTable.ui", self)

        self._model = model
        self._updating = False
        self._tables = []
        self._current_df_id = 0   

        self.saveButton.clicked.connect(self.alternatives_save_current_config)
        self.backButton.clicked.connect(callback_backButton)
        self.nextButton.clicked.connect(callback_nextButton)

        self.intervalComboBox.currentIndexChanged.connect(self._on_interval_changed)


    def init_intervals(self):
        """Llena el combo de intervalos según los datos disponibles y construye las tablas."""
        dfs_in_intervals = self._model.getDataframes_intervalList()
        if dfs_in_intervals is None:
            num_intervals = 0
        else:
            num_intervals = len(dfs_in_intervals)

        self.intervalComboBox.blockSignals(True)
        self.intervalComboBox.clear()
        for i in range(num_intervals):
            self.intervalComboBox.addItem(f"Intervalo {i+1}")
        self.intervalComboBox.blockSignals(False)

        if num_intervals > 0:
            self._current_df_id = 0
            self.intervalComboBox.setCurrentIndex(0)
            self.build_tables()
        else:
            # No hay intervalos, limpiar
            layout = self.criteriaContainer.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self._tables.clear()

    def _on_interval_changed(self, index):
        """Se activa al cambiar el intervalo seleccionado."""
        if index >= 0:
            self._current_df_id = index
            self.build_tables()


    def build_tables(self):
        """Crea un QGroupBox por cada criterio con su tabla para el intervalo actual."""
        layout = self.criteriaContainer.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._tables = []

        criteria = self._model.getCriteria()
        for crit in criteria:
            group = QGroupBox(f"Criterio: {crit.name}")
            vbox = QVBoxLayout()
            table = self._create_alternative_table(crit)
            vbox.addWidget(table)
            group.setLayout(vbox)
            layout.addWidget(group)
            self._tables.append(table)

        for table in self._tables:
            table.cellChanged.connect(self._on_cell_changed)
            table.horizontalHeader().sectionDoubleClicked.connect(
                self._edit_alternative_name)
            table.verticalHeader().sectionDoubleClicked.connect(
                self._edit_alternative_name)

    def _create_alternative_table(self, crit):
        """Crea una QTableWidget para comparar alternativas según un criterio y el df_id actual."""
        table = QTableWidget()
        alternatives = list(self._model.getAlternatives())
        n = len(alternatives)
        table.setRowCount(n)
        table.setColumnCount(n)
        table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.criterion = crit
        table.df_id = self._current_df_id   # guardamos el intervalo en la tabla

        for i, alt in enumerate(alternatives):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(alt.name))
            table.setVerticalHeaderItem(i, QTableWidgetItem(alt.name))

        self._updating = True
        for i, alt_i in enumerate(alternatives):
            for j, alt_j in enumerate(alternatives):
                weight = alt_i.getAltWeight_Crit_Alt(crit, alt_j, self._current_df_id)
                if weight is None:
                    # Si no existe relación, la creamos con peso 1
                    relateAlternatives(crit, alt_i, alt_j, self._current_df_id, 1.0)
                    weight = 1.0
                item = QTableWidgetItem(self._format_ahp_weight(weight))
                if i == j:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(i, j, item)
        self._updating = False

        table.horizontalHeader().setSectionsClickable(True)
        table.verticalHeader().setSectionsClickable(True)
        return table


    def _edit_alternative_name(self, index):
        """Renombra una alternativa en el modelo y en todas las tablas."""
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
        df_id = table.df_id
        alternatives = list(self._model.getAlternatives())
        alt_row = alternatives[row]
        alt_col = alternatives[col]

        alterAlternativesWeight(crit, alt_row, alt_col, df_id, val)

        self._updating = True
        new_weight_row_col = alt_row.getAltWeight_Crit_Alt(crit, alt_col, df_id)
        new_weight_col_row = alt_col.getAltWeight_Crit_Alt(crit, alt_row, df_id)

        table.item(row, col).setText(self._format_ahp_weight(new_weight_row_col))
        table.item(col, row).setText(self._format_ahp_weight(new_weight_col_row))
        self._updating = False


    def alternatives_save_current_config(self):
        self._model.saveAlternatives()


    @staticmethod
    def _format_ahp_weight(weight):
        if weight == int(weight):
            return str(int(weight))
        n_val = round(1.0 / weight) if weight != 0 else 1
        if abs(weight - 1.0 / n_val) < 1e-9 and 1 <= n_val <= 9:
            return f"1/{n_val}"
        return f"{weight:.3g}"
    

    def build_relations(self):
        dfs_in_intervals = self._model.getDataframes_intervalList()
        alternativesParams = self._model.getAlternativesParams()
        alternatives = self._model.getAlternatives()
        criteria = self._model.getCriteria()
        criteriaParams = self._model.getCriteriaParams()
        fuzzyCriteria = {}

        for crit in criteria:
            crit_alt_p = []
            for alt_p in alternativesParams:
                if alt_p.crit == crit.name:
                    crit_alt_p.append(alt_p)
            fuzzyCriteria[crit.name] = FuzzyCriteria(crit.name, crit_alt_p)
        
        saaty_values = []
        for i in range(1, 10):
            saaty_values.append(i)
            if i != 1:
                saaty_values.append(1 / i)

        for indx, dfs in enumerate(dfs_in_intervals):
            for crit in criteria:
                # Creamos las relaciones si no existen
                for alt_1 in alternatives:
                    for alt_2 in alternatives:
                        if not alt_1.hasAlternativeInRels(crit, alt_2, indx):
                            relateAlternatives(crit, alt_1, alt_2, indx, 1)
                
                # Obtenemos el valor del dataframe (media de pasos, maxima temp, etc)
                for crit_p in criteriaParams:
                    if crit_p.crit == crit.name:
                        crit_value = crit_p.useMethod(dfs)
                        break
                    
                if crit_value is None:
                    continue

                for alt in alternatives:
                    alt_value = fuzzyCriteria[crit.name].getMembershipValue(alt.name, crit_value)

                    # Iteramos por las relaciones de la alt actual (siempre que sean del criterio actual)
                    alt_rels = alt.getAlternativeRels()
                    for alt_rel in alt_rels:
                        if alt_rel.crit != crit or alt_rel.alt == alt or alt_rel.df_id != indx:
                            continue
                        alt_o_value = fuzzyCriteria[crit.name].getMembershipValue(alt_rel.alt.name, crit_value)

                        if alt_o_value == 0 and alt_value == 0:
                            weight = 1.0
                        elif alt_o_value == 0:
                            weight = 9.0
                        elif alt_value == 0:
                            weight = 1/9
                        else:
                            weight = alt_value / alt_o_value

                        # Calculamos el valor de Saaty extricto
                        trueWeight = 1.0
                        min_dist = float('inf')
                        for val in saaty_values:
                            dist = abs(weight - val)
                            if dist < min_dist:
                                min_dist = dist
                                trueWeight = val

                        alterAlternativesWeight(crit, alt, alt_rel.alt, indx, trueWeight)    