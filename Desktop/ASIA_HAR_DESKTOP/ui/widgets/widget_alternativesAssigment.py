from PyQt6 import uic
from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QVBoxLayout, QLabel,
    QDoubleSpinBox, QHBoxLayout, QPushButton, QInputDialog
)
from PyQt6.QtCore import Qt
from ui.config import RESOURCES_DIR

from core.alternative import *
from core.alternatives_data_params import *


class AlternativesAssigment(QWidget):
    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "alternativesAssigment.ui", self)

        self._model = model
        self._alternatives = []          # objetos Alternative
        self._criteria = []              # objetos Criteria
        self._alternatives_params = []           # dict: (alt.name, crit.name) -> [a, b, c, d]

        self.addAlternativeButton.clicked.connect(self._add_alternative)
        self.removeAlternativeButton.clicked.connect(self._remove_alternative)
        self.backButton.clicked.connect(callback_backButton)
        self.nextButton.clicked.connect(callback_nextButton)
        self.saveButton.clicked.connect(self._save_config)

    # ------------------------------------------------------------------
    # Carga desde el modelo
    # ------------------------------------------------------------------
    def load_from_model(self):
        self._alternatives = self._model.getAlternatives()
        self._criteria = self._model.getCriteria()
        self._alternatives_params = self._model.getAlternativesParams()
        
        sample_func = [0.0, 1.0, 2.0, 3.0]

        for alt in self._alternatives:
            alt_relations = alt.getAlternativeRels()
            for alt_rel in alt_relations:
                found = False
                for alt_p in self._alternatives_params:
                    if alt.name == alt_p.alt and alt_rel.crit.name == alt_p.crit:
                        found = True
                        if len(alt_p.func) == 0:
                            alt_p.func = sample_func.copy()
                if not found:
                    self._alternatives_params.append(AlternativesDataParams(alt.name, alt_rel.crit.name, sample_func.copy()))

        if not self._alternatives:
            self._add_alternative_to_model("Alternativa 1")
            self._add_alternative_to_model("Alternativa 2")
            self.load_from_model()
        
        self._model.updateAlternativesParams(self._alternatives_params)


    # ------------------------------------------------------------------
    # Construcción de la interfaz (MEJORADA)
    # ------------------------------------------------------------------
    def build_ui(self):
        layout = self.alternativesContainer.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for alt in self._alternatives:
            # Título nativo del QGroupBox = nombre de la alternativa
            group = QGroupBox(alt.name)
            group_vbox = QVBoxLayout()

            # --- Botón de renombrar (arriba a la derecha) ---
            rename_btn = QPushButton("✎ Renombrar")
            rename_btn.setFixedHeight(30)
            rename_btn.setStyleSheet("""
                QPushButton {
                    background-color: #80CBC4;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4DB6AC;
                }
            """)
            rename_btn.clicked.connect(lambda checked, a=alt: self._rename_alternative(a))
            h_rename = QHBoxLayout()
            h_rename.addStretch()
            h_rename.addWidget(rename_btn)
            group_vbox.addLayout(h_rename)

            # --- Filas de criterios con los cuatro puntos ---
            for crit in self._criteria:
                crit_layout = QHBoxLayout()
                label = QLabel(f"{crit.name}:")
                label.setFixedWidth(120)
                crit_layout.addWidget(label)

                points = None
                for alt_p in self._alternatives_params:
                    if alt.name == alt_p.alt and crit.name == alt_p.crit:
                        points = alt_p.func

                for i, punto in enumerate(points):
                    sb = QDoubleSpinBox()
                    sb.setRange(0.0, 100.0)
                    sb.setValue(punto)
                    sb.setSingleStep(0.5)
                    sb.setDecimals(1)
                    sb.valueChanged.connect(
                        lambda value, a=alt, c=crit, idx=i: self._update_point(a, c, idx, value)
                    )
                    crit_layout.addWidget(sb)
                group_vbox.addLayout(crit_layout)

            group.setLayout(group_vbox)
            layout.addWidget(group)

        layout.addStretch()


    # ------------------------------------------------------------------
    # Resto de métodos (sin cambios)
    # ------------------------------------------------------------------
    def _update_point(self, alt, crit, idx, value):
        for alt_p in self._alternatives_params:
            if alt_p.alt == alt.name and alt_p.crit == crit.name:
                alt_p.func[idx] = value
        self._model.updateAlternativesParams(self._alternatives_params)


    def _add_alternative_to_model(self, name):
        sample_func = [0.0, 1.0, 2.0, 3.0]

        new_alt = Alternative(name)

        for crit in self._criteria:
            self._alternatives_params.append(AlternativesDataParams(new_alt.name, crit.name, sample_func))
            for alt in self._alternatives:
                relateAlternatives(crit, new_alt, alt, 1.0)            
        self._alternatives.append(new_alt)

        self._model.updateAlternatives(self._alternatives)
        self._model.updateAlternativesParams(self._alternatives_params)


    def _add_alternative(self):
        n = len(self._alternatives) + 1
        base_name = f"Alternativa {n}"

        existing = [ alt.name for alt in self._alternatives ]
        name = base_name
        
        while name in existing:
            n += 1
            name = f"Alternativa {n}"
        
        self._add_alternative_to_model(name)
        self.load_from_model()
        self.build_ui()


    def _remove_alternative(self):
        if len(self._alternatives) <= 2:
            return
        
        alt = self._alternatives.pop()
        alt_relations = alt.getAlternativeRels()
        for alt_rel in alt_relations:
            unrelateAlternatives(alt_rel.crit, alt, alt_rel.alt)
        
        self._alternatives_params = [ x for x in self._alternatives_params if x.alt != alt.name ]

        self._model.updateAlternatives(self._alternatives)
        self._model.updateAlternativesParams(self._alternatives_params)

        self.load_from_model()
        self.build_ui()


    def _rename_alternative(self, alt):
        old_name = alt.name
        new_name, ok = QInputDialog.getText(
            self, "Renombrar alternativa",
            f"Nuevo nombre para '{old_name}':",
            text=old_name
        )

        if ok and new_name.strip():
            new_name = new_name.strip()
            if new_name == old_name:
                return
            
            if any(a.name == new_name for a in self._alternatives if a != alt):
                return
            
            alt.name = new_name
            for alt_p in self._alternatives_params:
                if alt_p.alt == old_name:
                    alt_p.alt = new_name

            self._model.updateAlternativesParams(self._alternatives_params)
            self._model.updateAlternatives(self._alternatives)
            self.build_ui()


    def _save_config(self):
        self._model.saveAlternativesParams()
        self._model.saveAlternatives()