# .py
# dependencies: matplotlib, numpy

import serial
import time
import array
import numpy as np
import matplotlib.pyplot as plt

PLT_TRAIL = 5
PLT_PAUSE = 0.0001

######## SERIAL SETUP

print("Enter the port name:")
PORT = input()
SER_FREQ = 9600

ser = serial.Serial(PORT, SER_FREQ, timeout=1)
time.sleep(1)

line = ser.readline()

######## CALIBRATION

base = [0]*5
vmin = [0]*5
vmax = [0]*5

resp = 'pinata'

# gather ambient values
while resp != "igloo":
	print("Please clear the surface to get ambient values. Enter 'igloo' when ready:")
	resp = input()

ser.read_all()
for i in range(100):
	line = ser.readline()
	string = line.decode().split(",")
	del string[-1]
	IR = [int(i) for i in string]
	base = np.add(IR, base)


# array of base (ambient) values, add this later to read values (but this is negative, so we're normalizing yes)
base = [int(-i/100) for i in base]
# print(base)

### get minimum distance sensed values
while resp != "capybara":
	print("Please place an obstacle as close to the sensors as possible. Enter 'capybara' when ready:")
	resp = input()

ser.read_all()
for i in range(100):
	line = ser.readline()
	string = line.decode().split(",")
	del string[-1]
	IR = [int(i) for i in string]
	vmax = np.add(IR, vmax)

### get maximum distance sensed values

vmax = [int(i/100) for i in vmax]
# print(vmax)

### get minimum distance sensed values
while resp != "haiku":
	print("Please place an obstacle as close to the edge of the sensing area (and away from sensors) as possible. Enter 'haiku' when ready:")
	resp = input()

ser.read_all()
for i in range(100):
	line = ser.readline()
	string = line.decode().split(",")
	del string[-1]
	IR = [int(i) for i in string]
	vmin = np.add(IR, vmin)

vmin = [int(i/100) for i in vmin]
# print(vmin)

######## CURVE FITTING and DIGITIZING

def arr2touch(IR):
	irmax = max(IR)
	
	irmaxi = -1
	for i in range(len(IR)):
		if(IR[i] == irmax):
			irmaxi = i
			break
	
	y = irmaxi
	x = -1
	if(irmax >= 0.7):
		x = 1
	elif irmax >= 0.15:
		x = 2
	elif irmax >= 0.025:
		x = 3
	elif irmax >= -0.015:
		x = 4
	elif irmax >= -0.035:
		x = 5
	print(irmax)
	return (x, 5-y)

######## GRAPHICS INIT

while resp != "start":
	print("Enter 'start' to start sensing")
	resp = input()

ser.read_all()

plt.ion()
fig = plt.figure()

x = []
y = []

try:
	######## SENSING
	while line:
		line = ser.readline()
		string = line.decode().split(",")
		del string[-1]
		IR = [int(i) for i in string]
		# print(np.subtract(IR, vmin)/np.subtract(vmax, vmin))
		coord = arr2touch(np.subtract(IR, vmin)/np.subtract(vmax, vmin))
		# print(coord)

		# Plotting
		plt.clf()
		if(coord[0] < 0 or coord[1] < 0):
			coord = (-1, -1)
		x.append(coord[0])
		y.append(coord[1])

		# Remove old entries
		if(len(x) > PLT_TRAIL):
			x = x[1:]
			y = y[1:]

		plt.plot(x, y, 'r')
		plt.plot(x, y, 'ro')
		plt.xlim([-1,5])
		plt.ylim([-1,5])
		plt.show()
		plt.pause(PLT_PAUSE)

except KeyboardInterrupt:
			print("\nExiting...")

######## EXEUNT

ser.close()


######## REFERENCES
# Graph drawing in Tkinter: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
	# Additional notes:
		# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
		# License: http://creativecommons.org/licenses/by-sa/3.0/	