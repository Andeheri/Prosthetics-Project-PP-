import sys
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
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-1, 1)
        
        self.canvas.draw()  # Perform an initial draw to cache the renderer
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1)  # Update every 1 ms
        
        self.current_value = 0

    def update_plot(self):
        self.current_value += 0.01
        if self.current_value > 10:
            self.timer.stop()
            return
        
        self.xdata.append(self.current_value)
        self.ydata.append(np.sin(self.current_value))
        self.line.set_data(self.xdata, self.ydata)
        
        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)
        self.canvas.flush_events()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = RealTimePlot()
    main.show()
    sys.exit(app.exec_())
