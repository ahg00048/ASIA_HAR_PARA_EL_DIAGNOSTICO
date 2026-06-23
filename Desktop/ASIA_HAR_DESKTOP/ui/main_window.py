import sys
from .config import *;
from model.mainModel import mainModel
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
from .widgets import widget_alternativesTable, widget_criteriaAssigment, widget_criteriaTable, widget_timeRange, widget_alternativesAssigment

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(RESOURCES_DIR / "mainwindow.ui", self)
        self.setWindowTitle("ASIA HAR DESKTOP")

        self._model = mainModel()
        
        self._timeRange = widget_timeRange.TimeRange(self.go_to_template, self.go_to_criteriaTable, self._model)
        self._criteriaTable = widget_criteriaTable.CriteriaTable(self.go_to_timeRange, self.go_to_criteriaAssigment, self._model)
        self._criteriaAssigment = widget_criteriaAssigment.CriteriaAssigment(self.go_to_criteriaTable, self.go_to_alternativesAssigment, self._model)
        self._alternativesAssigment = widget_alternativesAssigment.AlternativesAssigment(self.go_to_criteriaAssigment, self.go_to_alternativesTable, self._model)
        self._alternativesTable = widget_alternativesTable.AlternativesTable(self.go_to_alternativesAssigment, self.go_to_alternativesTable, self._model)
        
        self.stackedWidget.addWidget(self._timeRange)
        self.stackedWidget.addWidget(self._criteriaTable)
        self.stackedWidget.addWidget(self._criteriaAssigment)
        self.stackedWidget.addWidget(self._alternativesAssigment)
        self.stackedWidget.addWidget(self._alternativesTable)

        # Vista inicial
        self.go_to_timeRange()


    def go_to_template(self):
        pass


    def go_to_timeRange(self):
        self.stackedWidget.setCurrentIndex(0)


    def go_to_criteriaTable(self):
        self.stackedWidget.setCurrentIndex(1)


    def go_to_criteriaAssigment(self):
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.currentWidget().build_rows()


    def go_to_alternativesAssigment(self):
        self.stackedWidget.setCurrentIndex(3)
        self.stackedWidget.currentWidget().load_from_model()
        self.stackedWidget.currentWidget().build_ui()


    def go_to_alternativesTable(self):
        self.stackedWidget.setCurrentIndex(4)        

