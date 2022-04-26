import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
comp = 4
troyka = 17

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(8)]

GPIO.setup(troyka, GPIO.OUT, )
GPIO.setup(comp, GPIO.IN)

def abc(local):
    
    val = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for l in range(8):

        val[l] = 1
        
        GPIO.output(dac, val)
        time.sleep(0.005)
        if GPIO.input(comp) == False :
            val[l] = 0

    number = val[0]*128+val[1]*64+val[2]*32+val[3]*16+val[4]*8+val[5]*4+val[6]*2+val[7]
    return number


try:
    print("Начало зарядки")
    GPIO.output(troyka, 1)
    t = 0
    a = 0
    list = [0]
    
    with open("/home/b04-108/data.txt", "w") as outfile:
        local = time.time()
        while(a == 0):
            p = abc(local)
            GPIO.output(leds, decimal2binary(p))

            if p >= 249:
                a = 1
                print("Разрядка")
            t = t + 1 
            outfile.write(str(p))
            outfile.write('\n')

        GPIO.output(troyka, 0)

        while(a == 1) :
            p = abc(local)
            if p <= 3:
                a = 0
                print("Конец разрядки")
            time.sleep(0.25)
            t = t + 1
            outfile.write(str(p))
            outfile.write('\n')
    step = 3.3 / 256
    GPIO.output(leds, decimal2binary(p))
        

    with open("/home/b04-108/data.txt", "r") as outfile:
        for line in outfile:
            list.append(int(line))
    with open("settings.txt", "w") as sets:
        sets.write(str(0.005) + '\n' + str(step))
    print("Шаг квантования:", step, '\n', "Частота дискретизации: 0.005")

    plt.plot(list)
    plt.show()

    

finally:
     for i in dac:
        GPIO.output(i, 0)
