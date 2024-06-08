import sys
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RealTimePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Plot")
        self.setGeometry(100, 100, 800, 600)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        
        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot([], [], 'r-')
        self.ax.set_xlim(0, 1)  # Initially show the last 1 second
        self.ax.set_ylim(0, 3.3)  # Assuming the analog value range is 0 to 3.3V
        
        self.ax.grid(True)  # Enable grid

        self.canvas.draw()  # Perform an initial draw to cache the renderer
        self.start_time = time.time()

    def update_plot(self, analog_value):
        current_time = time.time() - self.start_time
        self.xdata.append(current_time)
        self.ydata.append(analog_value)
        
        # Keep only the last 1 second of data
        if current_time > 1:
            self.xdata = [t for t in self.xdata if t >= current_time - 1]
            self.ydata = self.ydata[-len(self.xdata):]
        print(len(self.ydata))
        self.line.set_data(self.xdata, self.ydata)
        self.ax.set_xlim(max(0, current_time - 1), current_time)  # Update x-axis to show the last 1 second
        
        # Redraw the grid
        self.ax.grid(True)
        
        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)
        self.canvas.flush_events()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = RealTimePlot()
    main_window.show()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Exiting program")
