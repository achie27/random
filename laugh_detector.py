"""
	Reference - Primary Detection Methods for Laugh Tracks by Keith Wilhelm

"""

import os, sys
import numpy as np
from scipy import signal
from moviepy.editor import VideoFileClip, concatenate_videoclips

import matplotlib.pyplot as plt

file = sys.argv[1].strip()
if not os.path.isfile(file):
	print("There is no " + file +"!")
	sys.exit()

file = VideoFileClip(file)
file.set_duration(int(file.duration))
file = file.resize((320, 240))
file_audio = file.audio
duration = int(file.duration)

avg_of_10ms=lambda i,f:np.sqrt((f.subclip(i, i+0.01).to_soundarray()**2).mean()) 
sig = [avg_of_10ms(i, file_audio) for i in np.arange(0.0, duration//1, 0.01)]

sig_len = len(sig)

freq = sig_len/int(file.duration)+0.0
t = np.arange(0, sig_len, 1)/freq

print("phasr")

hil_sig = signal.hilbert(sig)

sig_env = np.abs(hil_sig)

avg = np.mean(sig_env)
print(avg)
norm_env = [i/avg for i in sig_env]

b, a = signal.butter(3, 0.05)
smooth_env = signal.filtfilt(b, a, norm_env)

plt.plot(t, smooth_env)
plt.show()

#will find better ways to get this; although it works well
high = 1.8
low = 0.45

joke_times, clip, offset, i = [{'s':0, 'e':0}], 0, 0, 0
while i < sig_len:
	if smooth_env[i] >= high :
		
		if joke_times[-1]['e'] >= t[i]-5:
			joke_times[-1]['e'] = np.min([t[i]+2, duration])
		else :
			joke_times.append({
				's' : np.max([0, t[i]-2]),
				'e' : np.min([t[i]+2, duration])
			})
			
		while i < sig_len and smooth_env[i] >= low:
			joke_times[-1]['e'] = np.min([t[i]+2, duration])
			i+=1

	i+=1


# print(joke_times)

jokes = []
for obj in joke_times:
	jokes.append(file.subclip(obj['s'], obj['e']))

jokes = concatenate_videoclips(jokes)
jokes.write_videofile("jokes_in_"+file.filename, codec='libx264')