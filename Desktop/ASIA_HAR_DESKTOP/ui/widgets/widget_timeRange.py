from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDateTime

from ui.config import RESOURCES_DIR

class TimeRange(QWidget):
    def __init__(self, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "timeRange.ui", self)
        self.nextButton.clicked.connect(self.validate_and_forward)
        self._callback_next = callback_nextButton
        self._model = model

        # Limpiar operaciones asíncronas al cambiar fechas
        self.startDateTime.dateTimeChanged.connect(self._clear_async_operations)
        self.endDateTime.dateTimeChanged.connect(self._clear_async_operations)

        # Cargar tiempo guardado previamente
        timestamp_tuple = self._model.getTime()
        self.startDateTime.setDateTime(QDateTime.fromSecsSinceEpoch(timestamp_tuple[0]))
        self.endDateTime.setDateTime(QDateTime.fromSecsSinceEpoch(timestamp_tuple[0] + timestamp_tuple[1]))
        self.intervalSpinBox.setValue(timestamp_tuple[2])

        # Cargar selección de casa y versión (si el modelo lo persiste)
        # Por ahora, dejamos valores por defecto
        self.houseComboBox.setCurrentIndex(0)  # casa 2
        self.v1RadioButton.setChecked(True)

    def _clear_async_operations(self):
        self._model.cancelDataframes()

    def validate_and_forward(self):
        start = self.startDateTime.dateTime().toPyDateTime()
        end = self.endDateTime.dateTime().toPyDateTime()
        interval = self.intervalSpinBox.value()
        house_id = int(self.houseComboBox.currentText())
        version = 1 if self.v1RadioButton.isChecked() else 2

        if start >= end:
            self.errorLabel.setText("La fecha de inicio debe ser anterior a la de fin.")
            return

        diff_minutes = (end - start).total_seconds() / 60.0
        if diff_minutes < 30:
            self.errorLabel.setText("El intervalo mínimo es de 30 minutos.")
            return
        if diff_minutes > 10080:  # 7 días
            self.errorLabel.setText("El intervalo máximo es de 7 días.")
            return
        if interval < 1 or interval > 1440:
            self.errorLabel.setText("El intervalo debe estar entre 1 minuto y un día.")
            return

        start_ts = start.timestamp()
        end_ts = end.timestamp()

        # Guardar los nuevos valores en el modelo (suponiendo que tenga métodos setHouse y setVersion)
        self._model.setTime(start_ts, end_ts, interval)
        self._model.setHouseId(house_id)
        self._model.setVersion(version)
        self._model.saveTime()
        self._model.fetchDataframes()
        self._callback_next()