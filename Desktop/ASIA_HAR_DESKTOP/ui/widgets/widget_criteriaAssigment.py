from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt

from ui.config import RESOURCES_DIR
from core.criteria import Criteria, relateCriterias, alterCriteriasWeight, unrelateCriterias

class CriteriaAssigment(QWidget):
    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "criteriaAssigment.ui", self)  

        self._model = model
        self._rows = []  

        self._build_rows()

        self.backButton.clicked.connect(callback_backButton)
        self.nextButton.clicked.connect(callback_nextButton)
        self.saveButton.clicked.connect(self.save_config)

    def _build_rows(self):
        """Crea una fila por cada criterio con dos combos y una etiqueta de salida."""
        layout = self.criteriaContainer.layout()

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._rows.clear()

        criteria = self._model.getCriteria()  # lista de objetos Criteria
        parametros = ["Temperatura", "Humedad", "Presión", "Luz", "Movimiento"]
        metodos = ["Media", "Máximo", "Mínimo", "Desviación", "Último valor"]

        for crit in criteria:
            group = QGroupBox(f"Criterio: {crit.name}")
            vbox = QVBoxLayout()

            # Fila con combos
            hbox = QHBoxLayout()
            combo_param = QComboBox()
            combo_param.addItems(parametros)
            combo_metodo = QComboBox()
            combo_metodo.addItems(metodos)

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

    def save_config(self):
        # Aquí guardarías las selecciones en el modelo o un archivo
        config = []
        for crit, cp, cm, _ in self._rows:
            config.append({
                "criterio": crit.name,
                "parametro": cp.currentText(),
                "metodo": cm.currentText()
            })
        # Ejemplo: self._model.saveParametersConfig(config)
        print("Configuración guardada:", config)

    def get_selections(self):
        """Devuelve un diccionario con las selecciones actuales."""
        return {crit.name: (cp.currentText(), cm.currentText()) for crit, cp, cm, _ in self._rows}