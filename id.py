import serial
import serial.tools.list_ports
import threading

serial_instance = serial.Serial(port="COM8", baudrate=9600)

while True:
    if serial_instance.inWaiting():
        packet = serial_instance.readline()
        data = packet.decode("ascii")


th = threading.Thread(target = RFIDMain, daemon = True)