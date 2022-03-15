import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3


def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)

try:
    while True:
        for value in range(0,255):
            signal = decimal2binary(value)
            GPIO.output(dac, signal)
            print(value)
            time.sleep(0.0001)
        for value in range(255,0, -1):
            signal = decimal2binary(value)
            GPIO.output(dac, signal)
            print(value)
            time.sleep(0.0001)
except KeyboardInterrupt:
    print("The program was stoped by the keyboard")
else: 
    print("No exceptions")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")
