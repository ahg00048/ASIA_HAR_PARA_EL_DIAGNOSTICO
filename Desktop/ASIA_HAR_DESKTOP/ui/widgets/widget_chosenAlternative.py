from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from ui.config import RESOURCES_DIR
from core.ahp.ahp_analysis import (
    calculate_CI as calculate_CI_criteria,
    calculate_CR,
    check_Valid_CR,
    calculate_Alt_Result,
    calculate_Best_Alt,
    RANDOM_INDEX
)
# Nota: hemos renombrado la función de criterios para evitar colisión con la de alternativas.
# Si las funciones originales están en el mismo módulo, tendrás que diferenciarlas.
# Asumimos que están en un módulo ahp_analysis.py.


class ChosenAlernative(QWidget):
    def __init__(self, callback_back, callback_backHome,  model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "chosenAlternative.ui", self)

        self._model = model
        self.backButton.clicked.connect(callback_back)
        self.backHomeButton.clicked.connect(callback_backHome)


    def compute_and_display(self):
        criteria = self._model.getCriteria()
        alternatives = self._model.getAlternatives()

        if not criteria or len(alternatives) < 2:
            self.bestAlternativeLabel.setText("Datos insuficientes")
            return

        n_crit = len(criteria)
        crit_sums = []
        crit_weights = []
        ci_crit = self._calculate_ci_criteria(criteria, crit_sums, crit_weights)
        cr_crit = calculate_CR(ci_crit, n_crit) if n_crit > 2 else 0.0

        alt_weights_per_crit = []
        consistency_warnings = []
        for crit in criteria:
            sums = []
            weights = []
            ci_alt = self._calculate_ci_alternatives(crit, alternatives, sums, weights)
            alt_weights_per_crit.append(weights)
            if len(alternatives) > 2:
                cr_alt = calculate_CR(ci_alt, len(alternatives))
                if not check_Valid_CR(cr_alt):
                    consistency_warnings.append(
                        f"Matriz de '{crit.name}' inconsistente (CR={cr_alt:.3f})"
                    )

        global_scores = []
        for j, alt in enumerate(alternatives):
            local_weights = [alt_weights_per_crit[i][j] for i in range(n_crit)]
            score = calculate_Alt_Result(crit_weights, local_weights)
            global_scores.append(score)

        best_idx = calculate_Best_Alt(global_scores)
        best_alt = alternatives[best_idx]

        self.bestAlternativeLabel.setText(
            f"✅ {best_alt.name} (puntuación: {global_scores[best_idx]:.4f})"
        )

        table = self.resultsTable
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

        consistency_text = ""
        if n_crit > 2:
            consistency_text += f"• Consistencia criterios: CR = {cr_crit:.3f} "
            if check_Valid_CR(cr_crit):
                consistency_text += "(aceptable)"
            else:
                consistency_text += "(no aceptable)"
            consistency_text += "\n"
        for warn in consistency_warnings:
            consistency_text += f"• {warn}\n"
        self.consistencyLabel.setText(consistency_text.strip())

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

    def _calculate_ci_alternatives(self, crit, alternatives, sums, weights):
        n = len(alternatives)
        sums.clear()
        for alt_col in alternatives:
            total = 0.0
            for alt_row in alternatives:
                total += alt_row.getAltWeight_Crit_Alt(crit, alt_col)
            sums.append(total)

        weights.clear()
        for alt_row in alternatives:
            row_sum = 0.0
            for j, alt_col in enumerate(alternatives):
                row_sum += alt_row.getAltWeight_Crit_Alt(crit, alt_col) / sums[j]
            weights.append(row_sum / n)

        lambda_max = 0.0
        for i in range(n):
            lambda_max += sums[i] * weights[i]
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        return ci