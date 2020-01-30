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
	
class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		self.Pid_var = {
			#'Kp': 0.6*2.8, 'Kd': 2/2, 'Ki': 2/8,
			'Kp': 0.85, 'Kd': 0.11, 'Ki': 0,
			'L': 118, 'R': 32.5,
			'x_f': 250, 'y_f': 200, 'r_f': radians(270),
			#'x_f': 346, 'y_f': 161.88, 'r_f': radians(0),
			'E_x': 0, 'E_y': 0, 'Er_0': 0, 'Er_s': 0, 'Er_f': 0,
			'erprior_x': 0, 'erprior_y': 0, 'erprior_0': 0, 'erprior_s': 0, 'erprior_f': 0,
			'dt': 0.08,
			'k': 0
		}

	def listen(self, P, cam):
		
		self.sock.listen(5)
		client, address = self.sock.accept()
		print('Connection address:', address)
		
		Preal = self.listenToClient(client, address, P, cam)
		return Preal
	def listenToClient(self, client, address, P , cam):
		size = 4
		#out = cv2.VideoWriter('output.avi', -1, 20.0, (640,450))
		Preal = P[0]
		poin = P
		i = 0
		reach = 0
		#file = open('text.txt', 'w').close()
		while True:
			try:
				nucleo_data = client.recv(size)
				#print( ' pira apo client')
				if nucleo_data:
					#print(' dextika')
					x, y, r = led_detection_new.coordinates(cam)
					Pcurrent = np.array([x,y])
					Preal = np.vstack((Preal, Pcurrent))
					ret, fram = cam.read()
					fram=fram[0:450,0:680]
					#cv2.circle(fram,(500,200),7,(0,0,255),-1)
					#file = open('text.txt', 'a+')
					#string = str(r) + ',' + str(format(time.time(), '.3f')) + ',' + str(int(self.Pid_var['r_f'])) + '\n'
					#file.write(string)
					#file.close()
					if i <= (len(P)-1):
						[xf,yf] = poin[i]
					else :
						print("I reached the goal")
						#print(Preal)
						
						
						client.close()
						cam.release()
						#out.release()
						cv2.destroyAllWindows()
						
						break
					#out.write(fram)
					velocity,reach = self.pid_controller(x, y, radians(r), xf, yf)
					
					if reach == 1:
						i = i + 1
					#velocity = '$' + str(format(2.55, '.2f')) + '$' + str(format(2.556, '.2f')) + '\r\n'
					#print("Taxuthtes:" ,velocity, self.Pid_var['r_0'])
					client.send(velocity.encode('utf-8'))
					#print('estila')
			except:
				return  False
		return Preal
		client.close()


	def pid_controller(self, x, y, r, xf, yf):


		if self.Pid_var['k'] == 0 or self.Pid_var['k'] == 1 :
				self.Pid_var['x_0'] = x
				self.Pid_var['y_0'] = y
				self.Pid_var['r_0'] = atan2(+yf - self.Pid_var['y_0'], xf - self.Pid_var['x_0'])
				self.Pid_var['k'] += 1
		reach = 0
		e_x = xf - x
		e_y = yf - y
		er_0 = atan2(sin(self.Pid_var['r_0'] - r), cos(self.Pid_var['r_0'] - r))
		er_s = atan2(sin(self.Pid_var['r_0'] - r), cos(self.Pid_var['r_0'] - r))
		er_f = atan2(sin(self.Pid_var['r_f'] - r), cos(self.Pid_var['r_f'] - r))
		if abs(er_0) > radians(8) and self.Pid_var['k'] != 0 and (abs(e_x) > 35 or abs(e_y) > 35):
				rotr_0 = self.Pid_var['Kp'] * er_0 + self.Pid_var['Kd'] * (er_0 - self.Pid_var['erprior_0']) / self.Pid_var['dt'] + self.Pid_var['Ki'] * self.Pid_var['Er_0'] * self.Pid_var['dt']
				vr = -(rotr_0 * self.Pid_var['L']) / (4 * self.Pid_var['R'] * pi)*4
				vl = (rotr_0 * self.Pid_var['L']) / (4 * self.Pid_var['R'] * pi)*4
				if abs(vr) < 0.1 and abs(vl) < 0.1:
						vr = 0
						vl = 0
				#elif abs(vr) < 0.35:
						#vr = (vr/abs(vr))*0.7
						#vl = (vl/abs(vl))*0.7
				self.Pid_var['Er_0'] += er_0
				self.Pid_var['erprior_0'] = er_0
				print(1,self.Pid_var['k'])
		elif abs(e_x) > 25 or abs(e_y) >25:
				print(2)
				#v0 = 1*0.025*(math.hypot(e_x,e_y))
				v0 = 0.6
				vr = v0
				vl = v0

				if abs(vr) < 0.1 and abs(vl) < 0.1:
						vr = 0
						vl = 0
		else :
				vr = 0
				vl = 0
				reach = 1
				print(3)
				self.Pid_var['k'] = 0
		velocity = '$' + str(format(vr, '.2f')) + '$' + str(format(vl, '.2f')) + '\r\n'
		return velocity,reach
if __name__ == "__main__":
	print('initializing server\n')
	t = ThreadedServer('0.0.0.0', 3000)
	print('listening sockets\n')
	Pobs,_,cam = led_detection_new.findobs()
	print(Pobs)
	Pg = np.array([100,50])
	x, y,_ = led_detection_new.coordinates_st(cam,Pg)
	Ps = np.array([x, y])
	
	P, elax = potfield.potfield(Ps, Pg, Pobs)
	print(P)
	if elax == 1:
		print('bika se elaxisto')
	elif elax ==2:
		print('bika se elaxisto kai dn vrika diadiadromi')
	xobs = [Pobs[:,0]]
	yobs = [Pobs[:,1]]
	print(xobs)
	print(yobs)
	ax = plt.gca()
	ax.cla()
	circle1=plt.Circle((xobs[0][0], yobs[0][0]),110,color = 'k')
	circle2=plt.Circle((xobs[0][1], yobs[0][1]),90,color = 'k')
	circle3=plt.Circle((xobs[0][2], yobs[0][2]),90,color = 'k')
	ax.set_xlim((0, 640))
	ax.set_ylim((0, 450))
	ax.add_artist(circle1)
	ax.add_artist(circle2)
	ax.add_artist(circle3)
	ax.plot(P[:,0], P[:,1], 'bo-')
	plt.axes().set_aspect('equal')
	plt.show()
	
	Preal=t.listen(P, cam)
	print(Preal)
	ax = plt.gca()
	ax.cla()
	circle1=plt.Circle((xobs[0][0], yobs[0][0]),110,color = 'k')
	circle2=plt.Circle((xobs[0][1], yobs[0][1]),90,color = 'k')
	circle3=plt.Circle((xobs[0][2], yobs[0][2]),90,color = 'k')
	ax.set_xlim((0, 640))
	ax.set_ylim((0, 450))
	ax.add_artist(circle1)
	ax.add_artist(circle2)
	ax.add_artist(circle3)
	ax.plot(P[:,0], P[:,1], 'bo-')
	ax.plot(Preal[:,0], Preal[:,1], 'r-')
	plt.axes().set_aspect('equal')
	plt.show()


