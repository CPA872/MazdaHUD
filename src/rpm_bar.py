from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget


class RPMBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the minimum and maximum values for the RPM range
        self.min_rpm = 0
        self.max_rpm = 9000
        self.rpm = 0
        self.color = self._get_bar_color(self.rpm)
        
        self.setAutoFillBackground(True)

        self.setFixedSize(150, 150)

    def paintEvent(self, event):
        # Call the base class's paintEvent method
        super().paintEvent(event)

        # Create a QPainter object to draw on the widget
        painter = QPainter(self)

        # Set the color and width of the pen
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        # Calculate the dimensions of the bar graph
        bar_width = self.width() // 3
        bar_height = self.height() - 20
        bar_x = self.width() // 2 - bar_width // 2
        bar_y = 10

        # Calculate the height of the bar based on the RPM value
        rpm_range = self.max_rpm - self.min_rpm
        rpm_ratio = (self.rpm - self.min_rpm) / rpm_range
        bar_fill_height = int(bar_height * rpm_ratio)

        # Set the color of the bar based on the range of RPM values
        self.color = self._get_bar_color(self.rpm)
        painter.setBrush(QColor(*self.color))

        # Draw the bar graph
        painter.drawRect(bar_x, bar_y + bar_height - bar_fill_height, bar_width, bar_fill_height)

        # Calculate the position and height of each black line
        line_interval = int(bar_height / 8)
        line_height = line_interval // 2
        line_positions = [(bar_y + bar_height - line_interval * i - line_height) for i in range(1, 9)]

        # Draw the black lines
        for y in line_positions:
            painter.drawLine(bar_x, y, bar_x + bar_width, y)

    def update_rpm(self, rpm):
        # Update the RPM value
        self.rpm = rpm

        # Trigger a repaint of the widget
        self.update()

    def _get_bar_color(self, rpm):
        if rpm < 3000:
            return (0, 255, 0)  # Green
        elif rpm < 4500:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)  # Red