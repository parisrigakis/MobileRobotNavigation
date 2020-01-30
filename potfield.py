import numpy as np
import math
import matplotlib.pyplot as plt
import time
from numpy import ones,vstack
from numpy.linalg import lstsq,norm
import random

def potfield(Ps, Pg, Pob):
	tim = time.time()
	fgoal = 0
	while fgoal == 0:
		if time.time() - tim > 10 :
			elax = 2
			break
		P = np.vstack(([0, 0],Ps))
		i = 1
		lm = 0
		k=0
		elax = 0
		while (P[i] != Pg).any():
			#Target Field
			vg = np.subtract(Pg, P[i])
			dg = np.linalg.norm(vg)
			velg = 15*np.true_divide(vg, dg)
			vel = velg
			
			#Obstacle Field
			if lm == 1:
				k = 0
				vkonos = np.subtract(Pkonos, P[i])
				dkonos = np.linalg.norm(vkonos)
				anadeltkonos = np.true_divide(vkonos, dkonos)
				velkonos= -8*anadeltkonos
				vel = np.add(vel,velkonos)
			vob1 = np.subtract(Pob[0], P[i])
			dob1 = np.linalg.norm(vob1) - 120
			anadelt1 = np.true_divide(vob1, (dob1+120))
			vob2 = np.subtract(Pob[1], P[i])
			dob2 = np.linalg.norm(vob2) - 100
			anadelt2 = np.true_divide(vob2, (dob2+100))
			vob3 = np.subtract(Pob[2], P[i])
			dob3 = np.linalg.norm(vob3) - 100
			anadelt3 = np.true_divide(vob3, (dob3+100))
			if dob1 < 70 :
				velob1 = 150*(1/70 - 1/dob1 )*anadelt1
				vel = np.add(vel,velob1)
			if dob2 < 70 :
				velob2 = 150*(1/70 - 1/dob2 )*anadelt2
				vel = np.add(vel,velob2)
			if dob3 < 70:
				velob3 = 150*(1/70 - 1/dob3 )*anadelt3
				vel = np.add(vel,velob3)
			#Borderline fields
			dar = P[i][0] - 40
			anadeltar = np.array([-1, 0])
			ddex = 640 - P[i][0] - 40
			anadeltdex = np.array([1, 0])
			dkat = P[i][1] - 40
			anadeltkat = np.array([0, -1])
			dpan = 450 - P[i][1] - 40
			anadeltpan = np.array([0, 1])
			if dar < 50 :
				velar = 100*(1/50 - 1/dar )*anadeltar
				vel = np.add(vel,velar)
			if ddex < 50 :
				veldex = 100*(1/50 - 1/ddex )*anadeltdex
				vel = np.add(vel,veldex)
			if dkat < 50 :
				velkat = 100*(1/50 - 1/dkat )*anadeltkat
				vel = np.add(vel,velkat)
			if dpan < 50 :
				velpan = 100*(1/50 - 1/dpan )*anadeltpan
				vel = np.add(vel,velpan)
			#print(vel)
			#Moving
			try:
				th = math.atan2(vel[0][1], vel[0][0])
			except:
				th = math.atan2(vel[1], vel[0])
			if i > 1 :
				thdif = math.atan2(math.sin(thp - th), math.cos(thp - th))
				if abs(thdif) > math.radians(150) and lm == 0:
					lm = 1
					elax = 1
					thkonos = random.uniform(0, 2*math.pi)
					Pkonos = [(P[i][0] + math.cos(thkonos)), (P[i][1] + math.sin(thkonos))]
					k=1
			if k == 0:
				if dg >5 :
					Pnew = [(P[i][0] + 5*math.cos(th)), (P[i][1] + 5*math.sin(th))]
				else :
					Pnew = Pg
					fgoal = 1
				P = np.vstack((P, Pnew))
				i = i + 1
				thp = th
			if len(P) > 500:
				break
	P = velt(P, Pob)
	#P = P[1:len(P)]
	return P, elax

def velt(P, Pob):
	j= 0
	temni = 0
	Pvelt = P[1]
	x01 = Pob[0][0]
	y01 = Pob[0][1]
	x02 = Pob[1][0]
	y02 = Pob[1][1]
	x03 = Pob[2][0]
	y03 = Pob[2][1]
	ppre= Pvelt
	pnow = Pvelt
	for p in P[2:len(P)]:
		points = [(pnow[0],pnow[1]), (p[0],p[1])]
		x_coords, y_coords = zip(*points)
		A = vstack([x_coords,ones(len(x_coords))]).T
		m, c = lstsq(A, y_coords,None)[0]
		a = - m
		c = - c
		x1 = (x01 - a*y01 - a*c)/(a**2 + 1)
		x2 = (x02 - a*y02 - a*c)/(a**2 + 1)
		x3 = (x03 - a*y03 - a*c)/(a**2 + 1)
		el = min(p[0],pnow[0])
		meg = max(p[0],pnow[0])
		if el < x1 < meg:   #theli diorthosi
			dob1 = abs(a*x01 + y01 + c)/norm([a,1])
			if dob1 <130:
				temni = 1
		if el < x2 < meg:
			dob2 = abs(a*x02 + y02 + c)/norm([a,1])
			if dob2 <110:
				temni = 1
		if el < x3 < meg:
			dob3 = abs(a*x03 + y03 + c)/norm([a,1])
			if dob3 <110:
				temni = 1
		if temni == 1 :
			Pvelt = np.vstack((Pvelt, ppre))
			temni = 0
			pnow = ppre
		elif np.all(p == P[len(P)-1]):
			Pvelt = np.vstack((Pvelt, ppre))
		ppre = p
	return Pvelt








