import serial
import time
import serial.serialutil
import serial.tools.list_ports
from threading import Thread
from multiprocessing import Queue
from logger import print_error
from graph import RealTimePlot

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys

def main() -> None:
    # Serial connection
    port = "COM3"
    baudrate = 9600
    timeout = 1  # Seconds

    # Analog value
    max_value = 3.3
    min_value = 0
    num_values = 1023

    conversion_factor = (max_value - min_value) / num_values

    sampling_time = 20 * 10 ** -3

    ser = connect_to_serial(port, baudrate, timeout)
    if isinstance(ser, serial.serialutil.SerialException):
        quit()
    else:
        print(f"Successfully connected to port {port}")
    
    analog_value_queue = Queue()

    analog_signal_thread = Thread(target=recieve_analog_signal, args=(ser, analog_value_queue, conversion_factor, sampling_time / 2), daemon=True)
    analog_signal_thread.start()

    # Graph window
    app = QApplication(sys.argv)
    main_window = RealTimePlot()
    main_window.show()

    def update_plot():
        if not analog_value_queue.empty():
            analog_value = analog_value_queue.get()
            main_window.update_plot(analog_value)

    timer = QTimer()
    timer.timeout.connect(update_plot)
    timer.start(1)  # Update every 1 ms

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        ser.close()

def connect_to_serial(port: str, baudrate: int, timeout: int) -> serial.Serial | None:
    """
    Sets up connection to teensy board over serial connection.
    """
    try:
        return serial.Serial(port, baudrate, timeout=timeout)
    except serial.serialutil.SerialException as e:
        print_error(f"Board is not active on {port}, or port is already in use.")
        return e

def recieve_analog_signal(ser: serial.Serial, analog_value_queue: Queue, conversion_factor: float, sampling_time: float):
    """
    Reads analog value from teensy board, and converts bit-value to analog value.\\
    Blocks until it receives a value.
    """
    while True:
        while ser.in_waiting != 0:
            analog_value = round(conversion_factor * int(ser.readline().decode('utf-8').rstrip()), 3)
            print(f"{analog_value}V")
            analog_value_queue.put(analog_value)
        time.sleep(sampling_time)

if __name__ == '__main__':
    main()
