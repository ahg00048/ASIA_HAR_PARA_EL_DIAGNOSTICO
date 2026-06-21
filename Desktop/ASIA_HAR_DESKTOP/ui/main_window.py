import sys
from .config import *;
from model.crit_alt import Crit_Alt
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
from .widgets import widget_alternativesTable, widget_criteriaTable, widget_login, widget_patientsTable

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "mainwindow.ui", self)
        self.setWindowTitle("ASIA HAR DESKTOP")

        self._model = Crit_Alt()
        self._login = widget_login.Login()
        self._patientsList = widget_patientsTable.PatientsTable()
        self._criteriaTable = widget_criteriaTable.CriteriaTable(self.go_to_login, self.go_to_alternativesTable, self._model)
        self._alternativesTable = widget_alternativesTable.AlternativesTable(self.go_to_criteriaTable, self.go_to_alternativesTable, self._model)
        
        self.stackedWidget.addWidget(self._login)
        self.stackedWidget.addWidget(self._patientsList)
        self.stackedWidget.addWidget(self._criteriaTable)
        self.stackedWidget.addWidget(self._alternativesTable)

        # Vista inicial
        self.go_to_criteriaTable()



    def go_to_login(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.currentWidget()


    def go_to_patientsList(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.currentWidget()

    def go_to_criteriaTable(self):
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.currentWidget()


    def go_to_alternativesTable(self):
        self.stackedWidget.setCurrentIndex(3)        
        self.stackedWidget.currentWidget()