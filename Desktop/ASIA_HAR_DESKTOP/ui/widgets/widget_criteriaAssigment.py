from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt

from ui.config import RESOURCES_DIR
from core.criteria_data_params import CriteriaDataParams
from core.criteria import Criteria, relateCriterias, alterCriteriasWeight, unrelateCriterias

class CriteriaAssigment(QWidget):
    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "criteriaAssigment.ui", self)  

        self._model = model
        self._rows = []  

        self.backButton.clicked.connect(callback_backButton)
        self.nextButton.clicked.connect(callback_nextButton)
        self.saveButton.clicked.connect(self.save_config)

    def build_rows(self):
        """Crea una fila por cada criterio con dos combos y una etiqueta de salida."""
        layout = self.criteriaContainer.layout()

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._rows.clear()

        criteria = self._model.getCriteria()  
        criteria_params = self._model.getCriteriaParams()
        params = self._model.getDfsValidProperties()
        methods = self._model.getDfsMethods()

        for crit in criteria:
            group = QGroupBox(f"Criterio: {crit.name}")
            vbox = QVBoxLayout()

            # Fila con combos
            hbox = QHBoxLayout()
            combo_param = QComboBox()
            combo_param.addItems(params)
            combo_metodo = QComboBox()
            combo_metodo.addItems(methods)

            default_param = params[0]   
            default_method = methods[0]
            for cp in criteria_params:
                if cp.crit == crit.name:   
                    default_param = cp.param
                    default_method = cp.method
                    break

            combo_param.setCurrentText(default_param)
            combo_metodo.setCurrentText(default_method)

            hbox.addWidget(QLabel("Parámetro:"))
            hbox.addWidget(combo_param)
            hbox.addWidget(QLabel("Método:"))
            hbox.addWidget(combo_metodo)
            vbox.addLayout(hbox)

            # Etiqueta de salida
            output_label = QLabel("Seleccione parámetro y método")
            output_label.setObjectName("outputLabel")
            vbox.addWidget(output_label)

            group.setLayout(vbox)
            layout.addWidget(group)

            # Conectar cambios en los combos para actualizar la salida
            combo_param.currentTextChanged.connect(
                lambda text, cl=combo_param, cm=combo_metodo, ol=output_label: self._update_output(cl, cm, ol)
            )
            combo_metodo.currentTextChanged.connect(
                lambda text, cl=combo_param, cm=combo_metodo, ol=output_label: self._update_output(cl, cm, ol)
            )

            # Guardar referencias si necesitas acceder luego
            self._rows.append((crit, combo_param, combo_metodo, output_label))

        # Espacio final para que no quede pegado al borde
        layout.addStretch()

    def _update_output(self, combo_param, combo_metodo, output_label):
        param = combo_param.currentText()
        metodo = combo_metodo.currentText()
        output_label.setText(f"{param} → {metodo}")
        
        criteria_param = []
        for crit, cp, cm, _ in self._rows:
            criteria_param.append(CriteriaDataParams(cp.currentText(), cm.currentText(), crit.name))
        self._model.updateCriteriaParams(criteria_param)


    def save_config(self):
        criteria_param = []
        for crit, cp, cm, _ in self._rows:
            criteria_param.append(CriteriaDataParams(cp.currentText(), cm.currentText(), crit.name))

        self._model.updateCriteriaParams(criteria_param)
        self._model.saveCriteriaParams()