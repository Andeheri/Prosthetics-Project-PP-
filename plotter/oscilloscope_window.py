import time
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
import pyqtgraph as pg
from PyQt5.QtGui import QPalette, QColor, QMouseEvent
from PyQt5.QtCore import Qt, QPoint


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(58, 58, 58))
        self.setPalette(palette)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)  # Add margins around the layout

        self.title = QLabel("Oscilloscope", self)
        self.title.setStyleSheet("color: white; padding-left: 10px;")
        self.layout.addWidget(self.title)

        self.layout.addStretch()  # Add stretch to push the button to the right

        self.close_button = QPushButton("X", self)
        self.close_button.setFixedSize(20, 20)  # Set fixed size for the close button
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border-radius: 2px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        self.close_button.clicked.connect(self.parent.close)
        self.layout.addWidget(self.close_button)

        self.start = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.start:
            delta = QPoint(event.globalPos() - self.start)
            self.parent.move(self.parent.pos() + delta)
            self.start = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.start = None


class OscilloscopeWindow(QMainWindow):
    def __init__(self, period: float, sampling_dt: float):
        super().__init__()
        self.setWindowTitle("Oscilloscope")
        self.setGeometry(100, 100, 800, 600)

        # Make the window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set the background color of the main window to gray
        self.setStyleSheet("background-color: gray;")

        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Set the background color of the plot area to black
        self.plot_widget.setBackground('k')
        self.plot = self.plot_widget.plot(pen=pg.mkPen(color='turquoise'))
        self.plot_widget.setYRange(0, 3.3)  # Assuming the analog value range is 0 to 3.3V

        # Remove x-axis labels
        self.plot_widget.getAxis('bottom').setStyle(showValues=False)

        # Show grid
        self.plot_widget.showGrid(x=True, y=True, alpha=0.5)
        self.plot_widget.setLabel('left', 'Analog Value (V)')

        self.T = period
        self.sampling_dt = sampling_dt
        self.num_samples = int(self.T / self.sampling_dt)

        # Set the x-axis range to always show 1 second of data
        self.plot_widget.setXRange(0, self.T)

        self.xdata = np.linspace(0, self.T, self.num_samples)
        self.ydata = []
        self.start_time = time.time()

        # Add a button layout
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # Create and add buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_button.setStyleSheet(self.button_style())
        self.stop_button.setStyleSheet(self.button_style())

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

    def button_style(self):
        return """
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """

    def update_plot(self, analog_value):
        self.ydata.append(analog_value)

        if len(self.ydata) > self.num_samples:
            self.ydata = self.ydata[-self.num_samples:]

        try:
            self.plot.setData(self.xdata, self.ydata)
        except Exception as e:
            self.plot.setData(self.xdata[0:len(self.ydata)], self.ydata)
