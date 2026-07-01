from PyQt6 import uic
from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QGroupBox, QVBoxLayout,
    QLabel, QTableWidget
)
from PyQt6.QtCore import Qt
from ui.config import RESOURCES_DIR
from core.ahp.ahp_analysis import (
    calculate_CI,
    calculate_CR,
    check_Valid_CR,
    calculate_Alt_Result,
    calculate_Best_Alt,
    RANDOM_INDEX
)

class ChosenAlernative(QWidget):
    def __init__(self, callback_back, callback_backHome, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "chosenAlternative.ui", self)

        self._model = model
        self.backButton.clicked.connect(callback_back)
        self.backHomeButton.clicked.connect(callback_backHome)


    def compute_and_display(self):
        criteria = self._model.getCriteria()
        alternatives = self._model.getAlternatives()
        dfs_intervals = self._model.getDataframes_intervalList()
        num_intervals = len(dfs_intervals) if dfs_intervals is not None else 0

        if not criteria or len(alternatives) < 2 or num_intervals == 0:
            self._show_empty_message("Datos insuficientes o no hay intervalos disponibles.")
            return

        self._clear_results()

        # 1. Pesos de los criterios (no dependen del intervalo)
        n_crit = len(criteria)
        crit_sums = []
        crit_weights = []
        ci_crit = self._calculate_ci_criteria(criteria, crit_sums, crit_weights)
        cr_crit = calculate_CR(ci_crit, n_crit) if n_crit > 2 else 0.0

        # Mostrar consistencia global de criterios
        consistency_text = f"• Consistencia criterios: CR = {cr_crit:.3f} "
        if n_crit > 2:
            if check_Valid_CR(cr_crit):
                consistency_text += "(aceptable)"
            else:
                consistency_text += "(no aceptable)"
        self.consistencyLabel.setText(consistency_text)

        # 2. Para cada intervalo, calcular pesos locales de alternativas y resultado global
        layout = self.resultsContainer.layout()
        for df_id in range(num_intervals):
            # --- Pesos locales de alternativas por criterio para este df_id ---
            alt_weights_per_crit = []
            consistency_warnings = []
            for crit in criteria:
                sums = []
                weights = []
                ci_alt = self._calculate_ci_alternatives(crit, alternatives, sums, weights, df_id)
                alt_weights_per_crit.append(weights)
                if len(alternatives) > 2:
                    cr_alt = calculate_CR(ci_alt, len(alternatives))
                    if not check_Valid_CR(cr_alt):
                        consistency_warnings.append(
                            f"Matriz de '{crit.name}' inconsistente (CR={cr_alt:.3f})"
                        )

            # --- Puntuaciones globales ---
            global_scores = []
            for j, alt in enumerate(alternatives):
                local_weights = [alt_weights_per_crit[i][j] for i in range(n_crit)]
                score = calculate_Alt_Result(crit_weights, local_weights)
                global_scores.append(score)

            best_idx = calculate_Best_Alt(global_scores)
            best_alt = alternatives[best_idx]

            # Crear un QGroupBox para este intervalo
            group = QGroupBox(f"Intervalo {df_id+1}")
            vbox = QVBoxLayout()

            # Etiqueta con la mejor alternativa
            best_label = QLabel(f"✅ {best_alt.name} (puntuación: {global_scores[best_idx]:.4f})")
            best_label.setObjectName("bestAlternativeLabel")
            vbox.addWidget(best_label)

            # Tabla de resultados
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Alternativa", "Puntuación global"])
            table.setRowCount(len(alternatives))
            for i, alt in enumerate(alternatives):
                name_item = QTableWidgetItem(alt.name)
                score_item = QTableWidgetItem(f"{global_scores[i]:.4f}")
                if i == best_idx:
                    font = name_item.font()
                    font.setBold(True)
                    name_item.setFont(font)
                    score_item.setFont(font)
                    name_item.setForeground(Qt.GlobalColor.darkCyan)
                    score_item.setForeground(Qt.GlobalColor.darkCyan)
                table.setItem(i, 0, name_item)
                table.setItem(i, 1, score_item)
            table.resizeColumnsToContents()
            vbox.addWidget(table)

            # Si hay advertencias de consistencia, mostrarlas
            if consistency_warnings:
                warn_label = QLabel("\n".join(consistency_warnings))
                warn_label.setStyleSheet("color: #e67e22; font-style: italic;")
                vbox.addWidget(warn_label)

            group.setLayout(vbox)
            layout.addWidget(group)


    def _calculate_ci_criteria(self, criteria, sums, weights):
        n = len(criteria)
        sums.clear()
        for crit_col in criteria:
            total = 0.0
            for crit_row in criteria:
                total += crit_row.getCritWeight_Crit(crit_col)
            sums.append(total)

        weights.clear()
        for crit_row in criteria:
            row_sum = 0.0
            for j, crit_col in enumerate(criteria):
                row_sum += crit_row.getCritWeight_Crit(crit_col) / sums[j]
            weights.append(row_sum / n)

        lambda_max = 0.0
        for i in range(n):
            lambda_max += sums[i] * weights[i]
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        return ci
    

    def _calculate_ci_alternatives(self, crit, alternatives, sums, weights, df_id):
        n = len(alternatives)
        sums.clear()
        for alt_col in alternatives:
            total = 0.0
            for alt_row in alternatives:
                total += alt_row.getAltWeight_Crit_Alt(crit, alt_col, df_id)
            sums.append(total)

        weights.clear()
        for alt_row in alternatives:
            row_sum = 0.0
            for j, alt_col in enumerate(alternatives):
                row_sum += alt_row.getAltWeight_Crit_Alt(crit, alt_col, df_id) / sums[j]
            weights.append(row_sum / n)

        lambda_max = 0.0
        for i in range(n):
            lambda_max += sums[i] * weights[i]
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        return ci


    def _clear_results(self):
        """Elimina los widgets dinámicos de resultados previos."""
        layout = self.resultsContainer.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def _show_empty_message(self, message):
        """Muestra un mensaje cuando no hay datos suficientes."""
        self._clear_results()
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #e67e22; font-size: 16px;")
        self.resultsContainer.layout().addWidget(label)