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

	def listen(self):
		self.sock.listen(5)
		while True:
			client, address = self.sock.accept()
			print('Connection address:', address)
			client.settimeout(60)
			threading.Thread(target=self.listenToClient, args=(client, address)).start()

	def listenToClient(self, client, address):
		size = 4
		cam = led_detection_new.init_cam(640,480,30)
		#file = open('text.txt', 'w').close()
		while True:
			try:
				nucleo_data = client.recv(size)
				if nucleo_data:
					x, y, r = led_detection_new.coordinates(cam)
					#file = open('text.txt', 'a+')
					#string = str(r) + ',' + str(format(time.time(), '.3f')) + ',' + str(int(self.Pid_var['r_f'])) + '\n'
					#file.write(string)
					#file.close()
					velocity = self.pid_controller(x, y, radians(r))
					#velocity = '$' + str(format(2.55, '.2f')) + '$' + str(format(2.556, '.2f')) + '\r\n'
					print("Taxuthtes:" ,velocity, self.Pid_var['r_0'])
					client.send(velocity.encode('utf-8'))
			except:
				client.close()
				return False		
		client.close()

	def pid_controller(self, x, y, r):
		if self.Pid_var['k'] == 0 or self.Pid_var['k'] == 1 :
				self.Pid_var['x_0'] = x
				self.Pid_var['y_0'] = y
				self.Pid_var['r_0'] = atan2(+(self.Pid_var['y_f'] - self.Pid_var['y_0']), (self.Pid_var['x_f'] - self.Pid_var['x_0']))
				self.Pid_var['k'] += 1
		e_x = self.Pid_var['x_f'] - x
		e_y = self.Pid_var['y_f'] - y
		er_0 = atan2(sin(self.Pid_var['r_0'] - r), cos(self.Pid_var['r_0'] - r))
		er_s = atan2(sin(self.Pid_var['r_0'] - r), cos(self.Pid_var['r_0'] - r))
		er_f = atan2(sin(self.Pid_var['r_f'] - r), cos(self.Pid_var['r_f'] - r))
		if abs(er_0) > radians(5) and self.Pid_var['k'] != 0:
			vr = -(er_0/abs(er_0))*0.35
			vl = (er_0/abs(er_0))*0.35
		elif abs(e_x) > 20 or abs(e_y) >20:
			if (e_x+e_y)>0:
					vr = 0.35
					vl = 0.35
			else:
					vr = -0.35
					vl = -0.35
		else :
			vr = 0
			vl = 0
		velocity = '$' + str(format(vr, '.2f')) + '$' + str(format(vl, '.2f')) + '\r\n'
		return velocity	
if __name__ == "__main__":
	print('initializing server\n')
	t = ThreadedServer('0.0.0.0', 3000)
	print('listening sockets\n')
	t.listen()
