import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 23
ECHO_PIN = 24

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    timeout = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        if (time.time() - timeout) > 3:
            print("Timeout occurred while waiting for echo signal")
            return None
    pulse_start = time.time()

    timeout = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        if (time.time() - timeout) > 3:
            print("Timeout occurred while receiving echo signal")
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def main():
    while True:
        print("Starting")
        dist = get_distance()
        print("Distance:", str(dist), "cm")

if __name__ == "__main__":
    main()
