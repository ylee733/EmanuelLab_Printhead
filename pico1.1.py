from machine import Pin
import utime
import math
import random

########## printhead #############
pinDict = {}
pins = [4,5,6,7,9,10,11,12,13,14,15,16,17,19,20,21,22,24,25,26,27,29,31,32,34]
for pin in pins:
    pinDict[pin] = Pin(pin,Pin.OUT)
rewardPinOut = Pin(1,Pin.OUT) # reward window 
trialPin = Pin(0,Pin.OUT) # trial window

# licks = {
#     "trial1": [1.2, 1.8, 2.4, 3.1],
#     "trial2": [0.9, 1.5, 2.2],
#     "trial3": [0.7, 1.3, 2.0, 2.8],
# }

# trials = {
#     "trial1": [1.0, 2.0, 3.0],
#     "trial2": [0.5, 1.5, 2.5],
#     "trial3": [0.6, 1.6, 2.6],
# }

# result = {}

# for trial_id, trial_time_frames in time_frames.items():
#     licks = []
#     for frame in trial_time_frames:
#         for time in trials.get(trial_id, []):
#             if frame <= time < frame + 1.0:
#                 licks.append(time)
#     result[trial_id] = licks

# print(result)

####### parameters ###########
# Define parameters
tone_duration = 0.5  # seconds
Fs = 200
speed = 0.1 # in mm/s
time_stim = 1/speed 
overlap = 3 # #of pins to have activated at once
stimulus_duration = 7
pinOrder = [1, 13, 2, 14, 3, 15, 4, 16, 5, 17, 6, 18, 7, 19, 8, 20, 9, 21, 10, 22, 11, 23, 12, 24]
time_pin = (overlap * time_stim) / (24 + overlap - 1)
time_pin_samples = int(math.floor(time_pin * Fs)) ## time_pin_samples = int(np.floor(time_pin * Fs))
numSamples = int(time_stim*Fs)
stim = [[0] * numSamples for _ in range(24)] ## stim = np.zeros((24, numSamples))
revStim = stim[::-1] ## revStim = np.flip(stim)
trialstartTimestamps = []
# trialTimeFrame = []
# trialTimeFrame = [(i, j) for i, j in zip(trialstartTimestamps, trialEndTimestamps)]

file = open("trialStartTimestamps.txt","w")
file = open("trialEndTimestamps.txt","w")
file = open("trialstartTimestamps.txt","w")

####### printhead going different directions ###########


for sample in range(numSamples):
    for i, pin in enumerate(pins):
        pinDict[pin].value(stim[i,sample])
    utime.sleep(1/Fs)

for i in range(24): # for each pin
    if i == 0:
        indentStart = 0
    else:
        indentStart = int(math.floor((i - 1) / (24 + overlap - 1) * time_stim * Fs)) ## indentStart = int(np.floor((i-1)/(24+overlap-1) * time_stim * Fs))
    indentEnd = indentStart + time_pin_samples
    if indentEnd > time_stim * Fs:
        indentEnd = int(math.floor(time_stim * Fs - 1)) ## indentEnd = int(np.floor(time_stim * Fs - 1))
    stim[pinOrder[i]-1, indentStart:indentEnd] = 1

def stimDir1():
   global stim
   outputArray = stim
   for sample in range(outputArray.shape(1)):
    for pin in range(outputArray.shape(0)):
      if outputArray[pin,sample] == 1:
        pinDict[pin].high()
      else:
        pinDict[pin].low()
    utime.sleep(1/Fs)

def stimDir2():
   global revStim
   outputArray = revStim
   for sample in range(outputArray.shape(1)):
    for pin in range(outputArray.shape(0)):
      if outputArray[pin,sample] == 1:
        pinDict[pin].high()
      else:
        pinDict[pin].low()
    utime.sleep(1/Fs)
# try uarray if ^ does not work

########### run trial ###############

def runTrial():
  if trialPin.value(1):
    trialstartTimestamps.append(utime.ticks_ms())
    print("Trial begin")
  goTrial = random.randint(0, 1) ## goTrial = np.random.binomial(1,0.5) ## determine go vs no go
  if goTrial:
    stimDir1(0.5)
    rewardPinOut.value(1)
    utime.sleep(1) ## duration of reward window, interrupt this if lick
    rewardPinOut.value(0)
    utime.sleep(3)
  
  else:
    stimDir2(0.5)
    utime.sleep(5)
  trialPin.value(0)


file.write(str(trialstartTimestamps)+",")
file.flush()
# clears input buffer 

# main trial
for i in range(100):
    trial_id = "trial " + i 
   runTrial()

# sorts the trials into a dictionary within dictionaries
# trial_ids = []
# lick_times = []

dict = {}
for i, trial_id in enumerate(trial_ids):
    dict[trial_id] = {}
    dict[trial_id]['lick_times'] = lick_times[i]

def save_trial_data_to_json(trial_data, filename):
    with uio.open(filename, 'w') as file:
        # Serialize the trial_data dictionary to JSON
        json_data = json.dumps(trial_data)
        file.write(json_data)

trial_ids = []
lick_times = []
trial_data = {}

for i, trial_id in enumerate(trial_ids):
    trial_data[trial_id] = {
        'lick_times': lick_times[i],
    }

filename = "trial_data.json"
save_trial_data_to_json(trial_data, filename)
