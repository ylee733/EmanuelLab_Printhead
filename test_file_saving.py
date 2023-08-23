import utime
from machine import Pin

valve = Pin(16, Pin.OUT)
led = Pin(25, Pin.OUT)
lick = Pin(14, Pin.IN, Pin.PULL_DOWN)
trial_counter = 0
lickTimestamps = []
valveOpenTimestamps = []
trialEndTimestamps = []
trialData = {}

with open("trial_ids(4).txt", "w") as file:
    while True:
        if lick.value():
            lickTimestamps.append(utime.ticks_ms())
            led.toggle()
            valve.value(0)
            utime.sleep(2)
            valve.value(1)
            valveOpenTimestamps.append(utime.ticks_ms())
            utime.sleep(1)
            trialEndTimestamps.append(utime.ticks_ms())
            trial_counter += 1
            trialData[trial_counter] = {
                'lickTimestamps': lickTimestamps[-1],
                'valveOpenTimestamps': valveOpenTimestamps[-1],
                'trialEndTimestamps': trialEndTimestamps[-1]
            }
            
            file.write(f"Trial ID: {trial_counter}\n")
            file.write(f"Lick Times: {trialData[trial_counter]['lickTimestamps']}\n")
            file.write(f"Valve Open Times: {trialData[trial_counter]['valveOpenTimestamps']}\n")
            file.write(f"Trial End Times: {trialData[trial_counter]['trialEndTimestamps']}\n")
            file.write("\n")
            
            file.flush()
            utime.sleep(2)
