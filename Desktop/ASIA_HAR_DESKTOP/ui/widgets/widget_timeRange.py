from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDateTime
from datetime import datetime

from ui.config import RESOURCES_DIR

class TimeRange(QWidget):
    def __init__(self, callback_backButton, callback_nextButton, model):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "timeRange.ui", self)  # Ajusta la ruta según tu configuración
        self.backButton.clicked.connect(callback_backButton)
        self.nextButton.clicked.connect(self.validate_and_forward)
        self._callback_next = callback_nextButton
        self._model = model
        
        # Limpiar errores al cambiar fechas
        self.startDateTime.dateTimeChanged.connect(self._clear_error)
        self.endDateTime.dateTimeChanged.connect(self._clear_error)

        timestamp_tuple = self._model.getTime() 

        self.startDateTime.setDateTime(QDateTime.fromSecsSinceEpoch(timestamp_tuple[0]))
        self.endDateTime.setDateTime(QDateTime.fromSecsSinceEpoch(timestamp_tuple[0] + timestamp_tuple[1]))


    def _clear_error(self):
        self.errorLabel.setText("La fecha inicial tienes que ser antes que la final, y tiene que haber una diferencia de entre 30 min a 1 dia.")


    def validate_and_forward(self):
        start = self.startDateTime.dateTime().toPyDateTime()
        end = self.endDateTime.dateTime().toPyDateTime()
        
        if start >= end:
            self.errorLabel.setText("La fecha de inicio debe ser anterior a la de fin.")
            return
        
        diff_minutes = (end - start).total_seconds() / 60.0
        if diff_minutes < 30:
            self.errorLabel.setText("El intervalo mínimo es de 30 minutos.")
            return
        if diff_minutes > 1440:  # 24 horas
            self.errorLabel.setText("El intervalo máximo es de 24 horas.")
            return
        
        start = start.timestamp()
        end = end.timestamp()

        self._model.setTime(start, end)
        self._model.saveTime()
        # Si pasa las validaciones, llamar al callback con los valores
        self._callback_next()