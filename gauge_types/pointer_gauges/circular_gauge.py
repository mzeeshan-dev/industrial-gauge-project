from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

class CircularGauge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)

        self._min_value = 0
        self._max_value = 100
        self._value = 50
        self._start_angle = 135
        self._end_angle = 405
        self._needle_angle = self.value_to_angle(self._value)

        self._animation = QPropertyAnimation(self, b"needle_angle")
        self._animation.setDuration(600)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.setLoopCount(1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)  # Center the gauge
        painter.setPen(Qt.white)

        # Draw the outer circle (gauge background)
        radius = 90
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)

        # Draw scale (example)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(0, -radius - 10, f"{self._min_value}")

        # Draw the needle (indicator)
        painter.setPen(QColor(255, 0, 0))
        painter.rotate(self._needle_angle)
        painter.drawLine(0, 0, 0, -radius)

    def value_to_angle(self, value):
        if self._max_value == self._min_value:
            return self._start_angle
        ratio = (value - self._min_value) / (self._max_value - self._min_value)
        return self._start_angle + ratio * (self._end_angle - self._start_angle)

    def set_value(self, value, animate=True, duration=600, easing=QEasingCurve.OutCubic):
        clamped = max(self._min_value, min(self._max_value, value))
        target_angle = self.value_to_angle(clamped)
        self._value = clamped

        if not animate:
            self._needle_angle = target_angle
            self.update()
            return

        if self._animation.state() == QPropertyAnimation.Running:
            self._animation.stop()

        self._animation.setDuration(int(duration))
        self._animation.setEasingCurve(easing)
        self._animation.setStartValue(self._needle_angle)
        self._animation.setEndValue(target_angle)
        self._animation.start()

    def get_needle_angle(self):
        return self._needle_angle

    def set_needle_angle(self, angle):
        self._needle_angle = angle
        self.update()

    needle_angle = pyqtProperty(float, fget=get_needle_angle, fset=set_needle_angle)
