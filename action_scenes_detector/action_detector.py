import os, sys, cv2
import numpy as np 

if not os.path.isfile(sys.argv[1]):
	print("not a file!")
	sys.exit()
INF = 100
k, i, N = 8, 0, 320*240
a, b, s, T = 0.2, 0.1, 4, fps * 90
hist, fd, shots = [], [], []
file = cv2.VideoCapture(sys.argv[1])
while file.isOpened():
	suc, fr = file.read()
	if not suc:
		break
	fr = cv2.resize(fr, (320, 240))
	gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
	hist_fr = cv2.calcHist([gray_fr], [0], None, [256], [0, 256])
	if i >= k:
		fd += np.sum(np.abs(hist_fr - hist[i-k]))/(2*N) 
	hist.append(hist_fr)
	i+=1

cnt = 0
total_frames = i
diff_fd = np.diff(fd)
for i in range(1, total_frames-1):
	if fd[i]>a and fd[i]>fd[i-1] and fd[i]>fd[i+1] :
		shots += i
	if fd[i] > b and fd[i-1]>b:
		cnt+=1
	else:
		cnt=0
	if cnt>=s:
		cnt = 0
		shots += i-s 

key_frames = []
total_shots = len(shots)
for i in range(0, total_shots):
	pre = i == 0 and 0 or shots[i-1]
	key_frames += (shots[i]+pre)//2

D, delta = [], 0.3
for i in range(0, total_shots):
	lim, j = key_frames[i] + T, i+1
	while key_frames[j] <= lim:
		D += {
			'f1' : i,
			'f2' : j,
			'fd' : np.sum(np.abs(hist[j] - hist[i]))/(2*N),
		}
		j+=1
#sort
shot_scene = range(0, total_shots)
D.sort(key = lambda obj: obj['fd'])
for ob in D:
	if ob['fd']>delta:
		break
	shot_scene[ob['f1']] = ob['f1']
	shot_scene[ob['f2']] = ob['f1']

scenes = []
