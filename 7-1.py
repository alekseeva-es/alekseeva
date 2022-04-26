import RPi.GPIO
import time
import matplotlib.pyplot as plot

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
comp = 4
st=0.005
troyka = 17


RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(dac, RPi.GPIO.OUT)
RPi.GPIO.setup(leds, RPi.GPIO.OUT)
RPi.GPIO.setup(troyka, RPi.GPIO.OUT)
RPi.GPIO.setup(comp, RPi.GPIO.IN)

def dec2bin(n):
    RPi.GPIO.output(leds, [int(j) for j in bin(n)[2:].zfill(8)])


def adc():
    j = [int(j) for j in bin(0)[2:].zfill(8)]
    for i in range(8):
        j[i] = 1
        RPi.GPIO.output(dac, j)
        time.sleep(0.005)
        if RPi.GPIO.input(comp) == 0:
            j[i] = 0
        RPi.GPIO.output(leds, j)
    return ((j[0]*128+j[1]*64+j[2]*32+j[3]*16+j[4]*8+j[5]*4+j[6]*2+j[7])*3.3/256)


try:
    print("Начало зарядки")
    measurement = []
    t0 = time.time()
    RPi.GPIO.output(troyka, 1)
    while True:
        p = adc()
        if p<3.2:
            measurement.append(round(p/3.3*256))

        else:
            break
    RPi.GPIO.output(troyka, 0)
    print("Разрядка")
    while True:
        p = adc()
        if p>0.066:
            measurement.append(round(p/3.3*256))

        else:
            break
    t1 = time.time()
    t01 = t1 - t0
    print("Конец разрядки")


    with open("data.txt", "w") as out:
        out.write("\n".join([str(i) for i in measurement]))
        freq = t01 / len(measurement)
        step = 3.3 / 256
        fr = 1 / st

    with open("settings.txt", "w") as sets:
        sets.write(str(0.005) + '\n' + str(step))
    print("Шаг квантования:", step, '\n', "Частота дискретизации: 0.005")


    plot.plot(measurement)
    plot.show()

finally:
    RPi.GPIO.output(dac, 0)
    RPi.GPIO.output(troyka, 0)
    RPi.GPIO.cleanup()

