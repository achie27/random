import os, sys
import numpy as np
from scipy.signal import hilbert
from moviepy.editor import VideoFileClip, concatenate_videoclips

file = sys.argv[1].strip()
if not os.path.isfile(file):
	print("There is no " + file +"!")
	sys.exit()

file = VideoFileClip(file)
file = file.resize((320, 240))
file_audio = file.audio

clips = []
num_clips = 5
clip_size = file.duration//num_clips

for i in range(0, num_clips):
	if i==num_clips-1:
		clips.append(file_audio.subclip(i*clip_size, file_audio.duration))
	else:
		clips.append(file_audio.subclip(i*clip_size, (i+1)*clip_size))

sigs = [i.to_soundarray() for i in clips]
hil_sigs = [hilbert(i) for i in sigs]
sig_env = [np.abs(i) for i in hil_sigs]

freq = len(sigs[0])/clips[0].duration
t = [1000*np.arange(0, len(sigs[0]), 1) / freq, 1000*np.arange(0, len(sigs[-1]), 1) / freq]

print("phase 1")

#experiment
high = 0.2
low = 0.1

l, clip, offset = [{'s':0, 'e':0}], 0, 0
for clip in range(0, 5):
	i = 0
	while i < len(sig_env[clip]):
		# t[clip//4][i] += offset
		abs_val = np.sqrt(sig_env[clip][i][0]**2 + sig_env[clip][i][1]**2)
		if abs_val >= high :
			if l[-1]['e'] >= t[clip//4][i]-5000+offset:
				l[-1]['e'] = t[clip//4][i]+offset
			else :
				l.append({
					's' : t[clip//4][i]+offset,
					'e' : t[clip//4][i]+offset
				})
				
			while i < len(sig_env[clip]) and abs_val >= low:
				l[-1]['e'] = t[clip//4][i]+offset
				abs_val = np.sqrt(sig_env[clip][i][0]**2 + sig_env[clip][i][1]**2)
				i+=1
				# t[clip//4][i] += offset
		i+=1

	offset+=clips[clip].duration*1000

# print("phase 1")
# print(l)

jokes = []
for obj in l:
	jokes.append(file.subclip(obj['s']/1000, obj['e']/1000))

jokes = concatenate_videoclips(jokes)
jokes.write_videofile("jokes_in_" + file.filename, codec='libx264')