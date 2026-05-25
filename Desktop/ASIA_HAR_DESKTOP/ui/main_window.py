import sys
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from .widgets import widget_alternativesTable, widget_criteriaTable, widget_login, widget_patientsTable

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('', self)
        self.setWindowTitle("ASIA HAR DESKTOP")
        
        self.login = widget_login.Login()
        self.patientsList = widget_patientsTable.PatientsTable()
        self.criteriaTable = widget_criteriaTable.CriteriaTable()
        self.alternativesTable = widget_alternativesTable.AlternativesTable([])

        self.stackedWidget.addWidget(self.login)
        self.stackedWidget.addWidget(self.patientsList)
        self.stackedWidget.addWidget(self.criteriaTable)
        self.stackedWidget.addWidget(self.alternativesTable)


    def go_to_login(self):
        self.stackedWidget.setCurrentIndex(0)


    def go_to_patientsList(self):
        self.stackedWidget.setCurrentIndex(1)


    def go_to_criteriaTable(self):
        self.stackedWidget.setCurrentIndex(2)


    def go_to_alternativesTable(self):
        self.stackedWidget.setCurrentIndex(3)        