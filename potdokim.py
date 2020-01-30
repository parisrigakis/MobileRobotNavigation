import potfield
import socket
import threading
import serial
import time
import cv2
import numpy as np
import led_detection_new 
from math import sin
from math import cos
from math import atan2
from math import pi
from math import radians
from math import sqrt
from math import degrees
import math
import potfield
import matplotlib.pyplot as plt


Ps = np.array([550,60])
Pobs = np.array([[520, 300], [400, 250], [250, 200]])
Pg = np.array([280,370])
P, elax = potfield.potfield(Ps, Pg, Pobs)
print(P)
if elax == 1:
	print('bika se elaxisto')
xobs = [Pobs[:,0]]
yobs = [Pobs[:,1]]
print(xobs)
print(yobs)
print(len(P))
ax = plt.gca()
ax.cla()
circle1=plt.Circle((xobs[0][0], yobs[0][0]),120,color = 'r')
circle2=plt.Circle((xobs[0][1], yobs[0][1]),100,color = 'r')
circle3=plt.Circle((xobs[0][2], yobs[0][2]),100,color = 'r')
ax.set_xlim((0, 640))
ax.set_ylim((0, 450))
ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(circle3)
ax.plot(P[:,0], P[:,1], 'bo')
plt.axes().set_aspect('equal')
plt.show()