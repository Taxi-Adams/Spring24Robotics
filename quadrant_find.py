import serial
import tts

def get_serial() -> None:
    serial_port = '/dev/ttyUSB0'
    baud_rate = 115200

    ser = serial.Serial(serial_port, baud_rate)
    ser.readline()
    response = ser.readline()
    list_response = response.decode().split(',')
    while list_response[0] != '$KT0':
        response = ser.readline()
        list_response = response.decode().split(',')

    return([float(list_response[1]), float(list_response[2]),
             float(list_response[3]), float(list_response[4])])



def find_quadrant(coords: list) -> None:
    min_coord = min(coords)
    quadrant = coords.index(min_coord)
    tts.Speech().tts_input(str(quadrant))


    