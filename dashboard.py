from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout

from gauge_types.pointer_gauges.circular_gauge import CircularGauge

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gauge Dashboard")
        self.setMinimumSize(800, 600)

        grid = QGridLayout()
        grid.setContentsMargins(12, 12, 12, 12)
        grid.setSpacing(12)

        self.airspeed_gauge = CircularGauge(self)
        self.altitude_gauge = CircularGauge(self)
        self.vspeed_gauge = CircularGauge(self)  # placeholder; would be bar gauge in full impl

        grid.addWidget(self.airspeed_gauge, 0, 0)
        grid.addWidget(self.altitude_gauge, 0, 1)
        grid.addWidget(self.vspeed_gauge, 1, 0, 1, 2)

        # Theme toggle
        controls = QHBoxLayout()
        btn_light = QPushButton("Light Theme")
        btn_dark = QPushButton("Dark Theme")
        btn_light.clicked.connect(self.set_light_theme)
        btn_dark.clicked.connect(self.set_dark_theme)
        controls.addWidget(btn_light)
        controls.addWidget(btn_dark)
        grid.addLayout(controls, 2, 0, 1, 2)

        self.setLayout(grid)
        self.set_dark_theme()

        # Simulated data updates
        self._tick = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_simulated)
        self._timer.start(800)

    def _update_simulated(self):
        self._tick += 1
        val1 = 10 + (self._tick % 90)
        val2 = 20 + ((self._tick * 2) % 80)
        val3 = 40 + ((self._tick * 3) % 50)
        self.airspeed_gauge.set_value(val1, animate=True, duration=700)
        self.altitude_gauge.set_value(val2, animate=True, duration=700)
        self.vspeed_gauge.set_value(val3, animate=True, duration=700)

    def set_light_theme(self):
        self.setStyleSheet(
            """
            QWidget { background-color: #ffffff; color: #000000; }
            QPushButton { background: #f0f0f0; border: 1px solid #ccc; padding: 6px 10px; }
            QPushButton:hover { background: #e6e6e6; }
            """
        )

    def set_dark_theme(self):
        self.setStyleSheet(
            """
            QWidget { background-color: #1e1e1e; color: #f4f4f4; }
            QPushButton { background: #2a2a2a; border: 1px solid #444; color: #f4f4f4; padding: 6px 10px; }
            QPushButton:hover { background: #333; }
            """
        )
