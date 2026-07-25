# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import wave as wave

audio = 'frosti.wav'
clipstart = 10
clipduration = 3
step = 1000 

#opening up the audio .wav file and setting up the start time and duration of the clip we're looking for 

wav = wave.open(audio, 'r')

samplef = wav.getframerate()      
channels = wav.getnchannels()      
tframes = wav.getnframes()

raw_bytes = wav.readframes(tframes)
wav.close()
songsignal = np.frombuffer(raw_bytes, dtype=np.int16)

if channels == 2:
    songsignal = songsignal.reshape(-1,2)
    songsignal = (songsignal[:,0]/2 +songsignal[:,1]/2)

songsignal = songsignal.astype(float)

#getting the sample frequency channels and total samples then turning the signal's type into float
#the if condition checks if the file is stereo and turns it into mono

print("sample frequency:", samplef,"Hz")
print("signal length:", len(songsignal),"samples")
    

cstart = int(clipstart * samplef)
clength = int(clipduration * samplef)
clip = songsignal[cstart : cstart + clength]

#getting the clip start and length in samples instead of seconds 
#and getting the clip itself as an array of floats 

print("clip length:", clength, "samples")
print("clip position:", cstart,"samples,",clipstart,"seconds")

def onesidefft (s):
    n = len(s)
    fft = np.fft.fft(s)
    mag = np.abs(fft[ :n//2])
    return mag

#function to do onesided fourier transform

clipfft = onesidefft(clip)
freq_axis = np.fft.fftfreq(clength, d=1/samplef)[ : clength //2]

fulltime = np.arange(len(songsignal)) / samplef
cliptime = np.arange(clength) / samplef

#calculating the x axis of the three plots 

plt.figure()
plt.plot(fulltime,songsignal)
plt.title("Full signal in time domain")

plt.figure()
plt.plot(cliptime, clip)
plt.title("Query clip in time domain")

plt.figure()
plt.plot(freq_axis,clipfft)
plt.title("Query clip in frequency domain")




scores = []
pos = []
i = 0

while i + clength <= len(songsignal):
    
    window = songsignal[i : i + clength]
    winfft = onesidefft(window)
    
    #extracting window and getting the onesided fft of the window 
    
    dotprod = np.dot(clipfft,winfft)
    normalized = np.linalg.norm(clipfft) * np.linalg.norm(winfft)
    
    if normalized == 0:
        score = 0
    else:
        score = dotprod / normalized
    
    #if function to prevent dividing by zero
    
    scores.append(score)
    pos.append(i)
    i = i + step

    #putting the score and position into the arrays

scores = np.array(scores)
pos = np.array(pos)

#transforming the arrays into np arrays to do numpy operations on them

besti = np.argmax(scores)
bestscore = scores[besti]
detectedstart = pos[besti]
detectedsec = detectedstart / samplef

#getting the index of the best score and getting its position and start second

print("Detected position:", detectedstart, "samples or",round(detectedsec,3), "secs")
print("Best score:",round(bestscore,8))

scoresec = pos / samplef

plt.figure()
plt.plot(scoresec,scores)
plt.axvline(clipstart,color='purple', label = 'Actual position')
plt.axvline(detectedsec,color='red', label = 'Detected position')
plt.title("Similarity score against time")
plt.legend()
plt.show()


detectedclip = songsignal[detectedstart : detectedstart+clength]

plt.figure()
plt.subplot(2,1,1)
plt.plot(cliptime, clip)
plt.title("Original Clip starts at " + str(clipstart) + "s")
plt.subplot(2,1,2)
plt.plot(cliptime,detectedclip)
plt.title("Detected Clip starts at " + str(round(detectedsec,3)) + "s")













    
    
    
    
    
    
    
    
    

















