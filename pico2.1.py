import utime
from machine import Pin

########## parameters ###############
valvePinOut = Pin(16,Pin.OUT)
led = Pin(25,Pin.OUT)
lickPinIn = Pin(14,Pin.IN,Pin.PULL_DOWN)
rewardPinIn = Pin(15,Pin.IN,Pin.PULL_DOWN)
trialPin = Pin(0,Pin.IN)
interrupt_flag = 0
valveOpenDuration = 1
trialEndTimestamps = []
rewardwinOpenTimestamps = []
stimulusStartTimestamps = []
lickTimestamps = []
valveOpenTimestamps = []

file = open("lickTimestamps.txt","w")
file = open("valveOpenTimestamps.txt","w")
file = open("stimulusStartTimestamps.txt","w")
file = open("rewardwinOpenTimestamps.txt","w")
file = open("trialEndTimestamps.txt","w")

########## timing of reward, lick, valve, etc. ###############

timediff_rewardwin = utime.ticks_diff(rewardwinOpenTimestamps, stimulusStartTimestamps)
if timediff_rewardwin > 20:
    stimulusStartTimestamps = rewardwinOpenTimestamps # ?

timediff_lick = utime.ticks_diff(lickTimestamps, stimulusStartTimestamps)
if timediff_lick > 20:
    stimulusStartTimestamps = lickTimestamps

timediff_valve = utime.ticks_diff(valveOpenTimestamps, stimulusStartTimestamps)
if timediff_valve > 20:
    stimulusStartTimestamps = valveOpenTimestamps

timediff_trialEnd = utime.ticks_diff(trialEndTimestamps, stimulusStartTimestamps)
if timediff_trialEnd > 20:
    stimulusStartTimestamps = trialEndTimestamps

########## lick interrupt ############

if trialPin.value(1):
    rewardwinOpenTimestamps.append(utime.ticks_ms())
    stimulusStartTimestamps.append(utime.ticks_ms())
    def lickCallback(lickPinIn):
        global interrupt_flag
        lickTimestamps.append(utime.ticks_ms())
        interrupt_flag = 1
    lickPinIn.irq(trigger=lickPinIn.IRQ_RISING, handler=lickCallback)

def openValve(duration):
    valvePinOut.value(1)
    utime.sleep_ms(duration)
    valvePinOut.value(0)

while True:
    if interrupt_flag is 1:
        interrupt_flag = 0
        if (rewardPinIn.value is 1) & (utime.ticks_diff(utime.ticks_ms,valveOpenTimestamps[-1]) > 1000):
            valveOpenTimestamps.append(utime.ticks_ms())
            openValve(20)
            

############ lick valve #################
    trialPin.value(0)
    trialEndTimestamps.append(utime.ticks_ms())
    file.write(str(trialEndTimestamps)+",")
    file.write(str(rewardwinOpenTimestamps)+",")
    file.write(str(stimulusStartTimestamps)+",")
    file.write(str(lickTimestamps)+",")
    file.write(str(valveOpenTimestamps)+",")
    file.flush()
    file.close()
    utime.sleep(10)

###########################
