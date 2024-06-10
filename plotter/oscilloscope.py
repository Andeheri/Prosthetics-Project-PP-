import serial
import time
import serial.serialutil
import serial.tools.list_ports
from threading import Thread, Event
from multiprocessing import Queue
from logger import print_error
from oscilloscope_window import OscilloscopeWindow

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

    # Plotting parameters
    period = 1  # Seconds
    sampling_time = 10 * 10 ** -3  # Seconds

    ser = connect_to_serial(port, baudrate, timeout)
    if isinstance(ser, serial.serialutil.SerialException):
        quit()
    else:
        print(f"Successfully connected to port {port}")
    
    analog_value_queue = Queue()
    stop_flag = Event()

    analog_signal_thread = Thread(target=recieve_analog_signal, args=(ser, analog_value_queue, conversion_factor, sampling_time / 2, stop_flag), daemon = True)
    analog_signal_thread.start()

    # Graph window
    app = QApplication(sys.argv)
    main_window = OscilloscopeWindow(period, sampling_time)
    main_window.show()

    def update_plot():
        while not analog_value_queue.empty():
            analog_value = analog_value_queue.get()
            main_window.update_plot(analog_value)

    timer = QTimer()
    timer.timeout.connect(update_plot)
    timer.start(10)  # Update every 1 ms

    try:
        print("Starting oscilloscope")
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting program")
        stop_flag.set()
        analog_signal_thread.join()
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

def recieve_analog_signal(ser: serial.Serial, analog_value_queue: Queue, conversion_factor: float, sampling_time: float, stop_flag: Event):
    """
    Reads analog value from teensy board, and converts bit-value to analog value.\\
    Blocks until it receives a value.
    """
    while not stop_flag.is_set():
        while ser.in_waiting != 0:
            analog_value = conversion_factor * int(ser.readline().decode('utf-8').rstrip())
            analog_value_queue.put(analog_value)
        time.sleep(sampling_time)

if __name__ == '__main__':
    main()
