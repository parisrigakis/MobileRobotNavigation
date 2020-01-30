import cv2
import numpy as np
import math
import time

def find_front_back(min_dist,max_dist,led1,led2,led3):
	if min_dist == 'dist1' and max_dist == 'dist2': 
		return led2, led3
	elif min_dist == 'dist2' and max_dist == 'dist1':
		return led2, led1
	elif min_dist == 'dist2' and max_dist == 'dist3': 
		return led3, led1
	elif min_dist == 'dist3' and max_dist == 'dist2':
		return led3, led2
	elif min_dist == 'dist1' and max_dist == 'dist3':
		return led1, led3
	elif min_dist == 'dist3' and max_dist == 'dist1':
		return led1, led2
	return ((0,0),(0,0))


def init_cam(videoWidth, videoHeight, videoFPS):
	cam = cv2.VideoCapture(0)
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, videoWidth)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, videoHeight)
	cam.set(cv2.CAP_PROP_FPS, videoFPS)
	return cam

def coordinates_st(cam,Pg):
	
	ok, frame = cam.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray=gray[0:450,0:640] 
	min_val1, max_val1, min_loc1, led1 = cv2.minMaxLoc(gray)
	cv2.circle(gray,led1,11,(0,0,255),-1)
	min_val2, max_val2, min_loc2, led2 = cv2.minMaxLoc(gray)
	cv2.circle(gray,led2,11,(0,0,255),-1)
	min_val3, max_val3, min_loc3, led3 = cv2.minMaxLoc(gray)
	cv2.circle(gray,led3,11,(0,0,255),-1)
	dist1 = math.hypot(led2[0]-led1[0],led2[1]-led1[1])
	dist2 = math.hypot(led3[0]-led2[0],led3[1]-led2[1])
	dist3 = math.hypot(led3[0]-led1[0],led3[1]-led1[1])
	distances_dict = {'dist1':dist1, 'dist2':dist2, 'dist3':dist3}
	maximum = max(dist1,dist2,dist3)
	minimun = min(dist1,dist2,dist3)
	for i in distances_dict:
		if maximum == distances_dict[i]:
			max_dist = i
		if minimun == distances_dict[i]:
			min_dist = i
	front_point, back_point = find_front_back(min_dist,max_dist,led1,led2,led3)
	middle_point_x = ((front_point[0] - back_point[0])/3)*2 + back_point[0]
	middle_point_y = ((front_point[1] - back_point[1])/3)*2 + back_point[1]
	middle_point = [middle_point_x,middle_point_y]
	middle_point_1 = tuple(middle_point)
	print('x=',middle_point_x,'y=',middle_point_y)
	#cv2.putText(gray,'Front point:{0:2.1f}'.format(front_point),(0,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255),2)
	theta = math.atan2((front_point[1]-back_point[1]),(front_point[0]-back_point[0]))
	theta = math.degrees(theta)
	#cv2.putText(gray,'theta:{0:2.1f}'.format(theta),(0,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255),2)
	#cv2.circle(gray,front_point,10,(255,255,255),-1)
	#cv2.circle(gray,back_point,10,(255,110,110),-1)
	cv2.circle(gray,(int(middle_point_x),int(middle_point_y)),7,(0,0,255),-1)
	cv2.circle(gray,(Pg[0],Pg[1]),7,(255,255,255),-1)
	cv2.imshow('frame', gray)
	cv2.waitKey(-1)
	return middle_point_x, middle_point_y, theta

def coordinates(cam):
	
        ok, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray=gray[0:450,0:640] 
        min_val1, max_val1, min_loc1, led1 = cv2.minMaxLoc(gray)
        cv2.circle(gray,led1,11,(0,0,255),-1)
        min_val2, max_val2, min_loc2, led2 = cv2.minMaxLoc(gray)
        cv2.circle(gray,led2,11,(0,0,255),-1)
        min_val3, max_val3, min_loc3, led3 = cv2.minMaxLoc(gray)
        cv2.circle(gray,led3,11,(0,0,255),-1)
        dist1 = math.hypot(led2[0]-led1[0],led2[1]-led1[1])
        dist2 = math.hypot(led3[0]-led2[0],led3[1]-led2[1])
        dist3 = math.hypot(led3[0]-led1[0],led3[1]-led1[1])
        distances_dict = {'dist1':dist1, 'dist2':dist2, 'dist3':dist3}
        maximum = max(dist1,dist2,dist3)
        minimun = min(dist1,dist2,dist3)
        for i in distances_dict:
        	if maximum == distances_dict[i]:
        		max_dist = i
        	if minimun == distances_dict[i]:
        		min_dist = i
        front_point, back_point = find_front_back(min_dist,max_dist,led1,led2,led3)
        middle_point_x = ((front_point[0] - back_point[0])/3)*2 + back_point[0]
        middle_point_y = ((front_point[1] - back_point[1])/3)*2 + back_point[1]
        middle_point = [middle_point_x,middle_point_y]
        middle_point_1 = tuple(middle_point)
        print('x=',middle_point_x,'y=',middle_point_y)
        #cv2.putText(gray,'Front point:{0:2.1f}'.format(front_point),(0,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255),2)
        theta = math.atan2((front_point[1]-back_point[1]),(front_point[0]-back_point[0]))
        theta = math.degrees(theta)
        #cv2.putText(gray,'theta:{0:2.1f}'.format(theta),(0,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255),2)
        #cv2.circle(gray,front_point,10,(255,255,255),-1)
        #cv2.circle(gray,back_point,10,(255,110,110),-1)
        cv2.circle(gray,(int(middle_point_x),int(middle_point_y)),7,(0,0,255),-1)

        cv2.imshow('frame', gray)
        k = cv2.waitKey(1) & 0xff # Esc
        if k == 27 : return -1
        return middle_point_x, middle_point_y, theta

#cam = init_cam(640,480,30)
'''while True:
	x, y, r = coordinates(cam)	
	if cv2.waitKey(1) == 27: 
		break # esc to quit'''

#cam = init_cam(640,480,30)		
'''while True:

        ok, frame = cam.read()
        imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,63,127,0)
        _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        try:
                maxa = cv2.cv2.arcLength(contours[0], True)
                for c in contours:
                        if cv2.cv2.arcLength(c,True)>= maxa:
                                cnt = c
        
                cv2.drawContours(thresh, [cnt], 0, (0,255,0), 3)
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(thresh,(int(cx),int(cy)),7,(0,0,255),-1)
                cv2.imshow('frame', thresh)
        except:
                cv2.imshow('frame', thresh)
        #cv2.drawContours(thresh, contours, -1, (0,255,0), 3)
        cv2.imshow('frame', thresh)
        if cv2.waitKey(1) == 27: 
                break # esc to quit'''

def findobs():
    cam = init_cam(640,480,30)
    cxp = 0
    cyp = 0
    cx = 100
    cy = 100
    rad = 0
    tim = time.time()
    while True:
        if (time.time()- tim)>10:
            break
        ok, frame = cam.read()
        grays = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        grays=grays[0:450,0:640]
        ret,thresh = cv2.threshold(grays,80,160,0)
        _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        try:
                
                for c in contours:
                        rad = int((cv2.contourArea(c)/math.pi)**0.5)
                        peri = cv2.arcLength(c, True)
                        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                        if len(approx) != 4 and rad< 80 and rad > 50 :
                                cnt1 = c
                        elif len(approx) != 4 and rad<50 and rad > 40 :
                                cnt2 = c
                        elif len(approx) == 4 and rad <50 and rad > 40:
                                cnt3 = c
                cv2.drawContours(thresh, [cnt1], 0, (0,255,0), 3)
                cv2.drawContours(thresh, [cnt2], 0, (0,255,0), 3)
                cv2.drawContours(thresh, [cnt3], 0, (0,255,0), 3)
                M1 = cv2.moments(cnt1)
                M2 = cv2.moments(cnt2)
                M3 = cv2.moments(cnt3)
                cx1 = int(M1['m10']/M1['m00'])
                cy1 = int(M1['m01']/M1['m00'])
                cx2 = int(M2['m10']/M2['m00'])
                cy2 = int(M2['m01']/M2['m00'])
                cx3 = int(M3['m10']/M3['m00'])
                cy3 = int(M3['m01']/M3['m00'])
                rad1 = int((cv2.contourArea(cnt1)/math.pi)**0.5)
                rad2 = int((cv2.contourArea(cnt2)/math.pi)**0.5)
                rad3 = int((cv2.contourArea(cnt3)/math.pi)**0.5)
                Pob1 = np.array([cx1, cy1])
                Pob2 = np.array([cx2, cy2])
                Pob3 = np.array([cx3, cy3])
                Pob = np.vstack((Pob1, Pob2, Pob3))
                rad = np.array([rad1, rad2, rad3])
                print(rad)
                cv2.circle(thresh,(int(cx1),int(cy1)),7,(0,0,255),-1)
                cv2.circle(thresh,(int(cx2),int(cy2)),7,(0,0,255),-1)
                cv2.circle(thresh,(int(cx3),int(cy3)),7,(0,0,255),-1)
                break
        except:
                b = 0
			
        
    cv2.imshow('frame', thresh)
    cv2.waitKey(-1)
    return Pob,rad,cam