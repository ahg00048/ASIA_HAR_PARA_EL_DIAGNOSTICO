import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
import asyncio
from qasync import QEventLoop, QApplication

from ui.widgets import widget_alternativesTable, widget_criteriaTable
from ui.main_window import Main_window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    loop = QEventLoop(app)
    
    asyncio.set_event_loop(loop)
    
    window = Main_window()
    window.show()
    
    with loop:
        loop.run_forever()