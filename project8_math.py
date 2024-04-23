import serial
import tts
import math
import time
from tango import Tango

def get_serial() -> None:
    serial_port = '/dev/ttyUSB0'
    #serial_port = '/dev/ttyACM0'
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


# returns an angle in degrees
def calc_angle(bottomLeft, bottomRight):
    # define constant base to be the sensor's reading of 2 to 1 distance (approx)
    base = 3.0
    print("calc angle bottomLeft: " + str(bottomLeft))
    print(", calc angle bottomRight: " + str(bottomRight))
    # phi is the angle from base to left wall
    phi = math.acos(((bottomLeft * bottomLeft + 9.0 - bottomRight * bottomRight) / (2 * base * bottomLeft))) * 180 / math.pi
    return phi

# returns a 2D vector
def calc_position(hypotenuse, phi):
    xDist = hypotenuse * math.cos(phi* math.pi / 180.0)
    yDist = hypotenuse * math.sin(phi * math.pi / 180.0)
    position = [xDist, yDist]
    return position
    
# returns an angle in degrees
def calc_turn_angle(firstPt, secondPt):
    facingX = firstPt[0] - secondPt[0]
    facingY = firstPt[1] - secondPt[1]
    normFactor = math.sqrt(facingX * facingX + facingY * facingY)
    if(normFactor == 0):
        print("The ****ing wheel isn't working again. Expect an error.")
    # normalized vector of which way the robot is facing
    dirFacing = [facingX / normFactor, facingY / normFactor]
    # using the unit circle to calculate the angle needed to turn to face exactly 'West'
    # the angle is the angle turned from west ccw, so turning cw that much should give exactly west
    angle = math.atan2(dirFacing[1], dirFacing[0]) * 180.0 / math.pi
    if(angle < 0):
        angle = 360.0 + angle
    return angle

def main():
    # initialize bot
    bot = Tango()
    #bot.turn_waist(6300)
    #bot.turn_lr(5900)
    #bot.turn_lr(6900)
    #time.sleep(1.5)
    #bot.stop_wheels_lr()
    # get distances
    coords = get_serial()
    d1 = coords[0]
    d2 = coords[1]
    d3 = coords[2]
    d4 = coords[3]
    # find the current quadrant and report it vocally
    find_quadrant(coords)
    isNorth = False
    isSouth = False
    min_coord = min(coords)
    quadrant = coords.index(min_coord)
    if(quadrant == 1 or quadrant == 2):
        isSouth = True
        isNorth = False
    elif(quadrant == 0 or quadrant == 3):
        isSouth = False
        isNorth = True
    positionAngle = calc_angle(d3, d2)
    [x, y] = calc_position(d3, positionAngle)
    # move backwards slowly
    time.sleep(2.0)
    bot.move_fb(5900)
    bot.move_fb(7000)
    time.sleep(1.3)
    bot.stop_wheels_fb()
    # get new distances and position
    coords2 = get_serial()
    d1Next = coords2[0]
    d2Next = coords2[1]
    d3Next = coords2[2]
    d4Next = coords2[3]
    phi = calc_angle(d3Next, d2Next)
    [x2, y2] = calc_position(d3Next, phi)
    firstPoint = [x, y]
    secondPoint = [x2, y2]
    print("first point:" + str(x) + ", " + str(y))
    print ("second point: " + str(x2) + ", " + str(y2))
    # calculate the current angle ccw from 90 degrees
    turnAngle = calc_turn_angle(firstPoint, secondPoint)
    print("I need to turn " + str(turnAngle) + " degrees")
    if(isSouth):
        turnAngle = 90.0 + turnAngle
        fraction = turnAngle / 360.0
        bot.turn_lr(5900)
        bot.turn_lr(4500)
        time.sleep(fraction * 2.433)
        bot.stop_wheels_lr()
        bot.move_fb(4900)
        time.sleep(1.95)
        bot.stop_wheels_fb()
    elif(isNorth):
        turnAngle = -90.0 + turnAngle
        fraction = turnAngle / 360.0
        bot.turn_lr(5900)
        bot.turn_lr(4500)
        time.sleep(fraction * 2.433)
        bot.stop_wheels_lr()
        bot.move_fb(4900)
        time.sleep(1.95)
        bot.stop_wheels_fb()
    tts.Speech().tts_input("I exited the zone")

if __name__ == "__main__":
   main()        
    
    
    
    