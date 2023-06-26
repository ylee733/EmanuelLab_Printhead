############## when to give reward ############
rewardPinIn = Pin(1, Pin.IN)
valvePinOut = Pin(0,Pin.OUT)
lickPinIn = Pin(4,Pin.IN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lickPinIn, GPIO.IN)
GPIO.setup(rewardPinIn, GPIO.IN)
GPIO.setup(valvePinOut, GPIO.OUT)
while True:
    # lickPinIn = GPIO.input(lickPinIn)
    # rewardPinIn = GPIO.input(rewardPinIn)
    # valvePinOut = GPIO.output(valvePinOut)
    if lickPinIn == GPIO.HIGH and rewardPinIn == GPIO.HIGH:
        GPIO.output(valvePinOut, GPIO.HIGH)
    else:
        GPIO.output(valvePinOut, GPIO.LOW)
    utime.sleep(10)
    # if abortIn == GPIO.HIGH and lickPinIn == GPIO.HIGH:
        # utime.sleep(10)
## interupt
# if a value change, do a sequence of event
# check the value of reward pin
# if high -> reward,record time,save
################ interrupt when lick #############################
lickPinIn = 0
debounce_time = 0
pin = Pin(4, Pin.IN, Pin.PULL_DOWN)
valvePinOut = Pin(0,Pin.OUT)
count=0
lickTimestamps = []
def lickCallback():
    lickTimestamps.append(utime.time())
    global lickPinIn, debounce_time
    if (time.ticks_ms()-debounce_time) > 100:
        lickPinIn = 1
        debounce_time = time.ticks_ms()
# pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)
while True:
     if lickPinIn == GPIO.HIGH and rewardPinIn == GPIO.HIGH:
        GPIO.output(valvePinOut, GPIO.HIGH)
        utime.sleep(valveOpenDuration)
        GPIO.output(valvePinOut, GPIO.LOW)
        print("Lick Detected")
        np.save('filenameTBD.npy',np.array(lickTimestamps))
#########################################################
## key items to save
# lick times
# trial starts
# reward window (maybe base on trial starts)
# trial identity (go/nogo)
