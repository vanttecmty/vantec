'''
	@name       	main.py
    @desc 			Navigation file. Definition and execution of threads and manipulation of components. 
	@author 		Marcopolo Gil Melchor marcogil93@gmail.com
	@created_at 	2017-06-05 
	@updated_at 	2017-11-28 Restructuration and comments. 
	@dependecies	python3
'''

'''
	Required python libraries 
'''
#Add python3 path
import os
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')

#For multithreading
import threading

#Basic libraries
import time
import math
import random
import datetime

#N-dimensional array object for images, radar drawing
import numpy as np

#opencv
import cv2 

#For image manipulations
from scipy import misc
from scipy.ndimage import rotate

'''
	Required our project libraries 
''' 
import motors as motors.Motors
import imu.Imu as Imu
import xbee.Xbee as Xbee
import lidar.Lidar as Lidar


class Radar:
	def __init__(self):
		frame = None;
		emptyMap = self.new_map(MAP_WIDTH, MAP_HEIGHT);
		routeMap = emptyMap.copy();


	def print_map(self, lidarObstacles, cameraObstacles):
			#Clean map
			routeMap = emptyMap.copy();

			for measure in LlidarObstacles:
				data = measure.split(",");
				#print(measure);
				degree = int(data[0]);
				distance = int(data[1]);

				if (degree > 0 and degree < 90) or (degree > 270 and degree < 360):
					#pasar de milimetros a centimetros -> dividir entre 10
					pixelX = LIDAR_COORD_X + int(math.cos(math.radians(degree - 90)) * float(distance/10) /2);
					pixelY = LIDAR_COORD_Y + int(math.sin(math.radians(degree - 90)) * float(distance/10) /2);
					#print(pixelX, pixelY);
					cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			self.add_boat(routeMap);	
			cv2.imshow('Route', routeMap);
			cv2.waitKey(100);
		print("End thread Map");

	def new_map(self, rows, cols):
		mapa = np.full((rows, cols, 3),0, dtype = np.uint8);
		return mapa;

	def add_boat(self, mapa):
		cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);	
#Roboat library
#import lib.roboBoatboat as boat

'''
	MAP THREAD CONSTANTS

	Rada dimension, objects scaled size, centroide coordenates
	
	The resolution of the radar is 10 meters.
'''
MAP_WIDTH       = 1000;
MAP_HEIGHT      = 1000;
BOUY_RADIOUS    = 6;
BOAT_HEIGHT     = 58;
BOAT_WIDTH      = 34;
BOAT_X1         = int(MAP_WIDTH/2 - BOAT_WIDTH/2);
BOAT_Y1         = int(MAP_HEIGHT/2 - BOAT_HEIGHT/2);
BOAT_X2         = int(MAP_WIDTH/2 + BOAT_WIDTH/2);
BOAT_Y2         = int(MAP_HEIGHT/2 + BOAT_HEIGHT/2);
LIDAR_COORD_X   = 100;
LIDAR_COORD_Y   = int(100 - BOAT_HEIGHT / 2);#200

#variable to stop program
runProgram        = True;

#camera variables
frame             = None;
capture           = None;

#maps and image variables 
destinyCoords     = [0,0];
routePoints       = [];
lidarObstacles    = [];
pixelsGoal        = [0,0];

orientationDegree = 0;




class MapThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name = name;

	def run(self):
		global routeMap, orientationDegree, frame;

		emptyMap = self.new_map(MAP_WIDTH, MAP_HEIGHT);
		routeMap = emptyMap.copy();

		while runProgram:
			routeMap = emptyMap.copy();

			'''
			'Set lidar obstacles in the map 
			''' 
			for measure in Lidar.obstacles:
				data = measure.split(",");
				#print(measure);
				degree = int(data[0]);
				distance = int(data[1]);

				if (degree > 0 and degree < 90) or (degree > 270 and degree < 360):
					#pasar de milimetros a centimetros -> dividir entre 10
					pixelX = LIDAR_COORD_X + int(math.cos(math.radians(degree - 90)) * float(distance/10) /2);
					pixelY = LIDAR_COORD_Y + int(math.sin(math.radians(degree - 90)) * float(distance/10) /2);
					#print(pixelX, pixelY);
					cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);
					cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);

			self.add_boat(routeMap);	
			cv2.imshow('Route', routeMap);
			cv2.waitKey(100);
		print("End thread Map");

	def new_map(self, rows, cols):
		mapa = np.full((rows, cols, 3),0, dtype = np.uint8);
		return mapa;

	def add_boat(self, mapa):
		cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);	

class NavigationThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self);
		self.threadID = threadID;
		self.name     = name;
	def run(self):
		global orientationDegree, destinyCoords, frame;
		self.go_to_destiny(29.151322, -81.017508);

	def go_to_destiny(self, latitude2, longitud2):
		global destiny;
		destiny               = imu.get_degrees_and_distance_to_gps_coords(latitude2, longitud2);
		orientationDegree     = destiny['degree'];
		lastOrientationDegree = orientationDegree;
		turn_degrees_needed   = orientationDegree;
		turn_degrees_accum    = 0;
		#clean angle;
		imu.get_delta_theta();

		#Condition distance more than 2 meters. 
		while destiny['distance'] > 3 and runProgram:
			#print("degrees: ", imu.NORTH_YAW);
			#print("coords: ", imu.get_gps_coords());
			print("destiny: ", destiny);
			#print("orientation degrees", orientationDegree);
			if(lastOrientationDegree != orientationDegree):
				turn_degrees_needed = orientationDegree;
				turn_degrees_accum  = 0;

				#clean angle;
				imu.get_delta_theta();
				lastOrientationDegree = orientationDegree;

			#If same direction, keep route
			#while math.fabs(turn_degrees_needed) > 10:
			imu_angle = imu.get_delta_theta()['z']%360;

			if(imu_angle > 180):
				imu_angle = imu_angle -360;
			#print("grados imu: ", imu_angle);

			#threshold
			if(math.fabs(imu_angle) > 1):
				turn_degrees_accum += imu_angle;

			#print("grados acc: ", turn_degrees_accum);
			turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360;

			if(turn_degrees_needed > 180): 
				turn_degrees_needed = turn_degrees_needed - 360;
			elif (turn_degrees_needed < -180):
				turn_degrees_needed = turn_degrees_needed + 360;
			
			#print("grados a voltear: ", turn_degrees_needed);

			if(math.fabs(turn_degrees_needed) < 10): 
				print("Tengo un margen menor a 10 grados");
				velocity = destiny['distance'] * 10;

				if (velocity > 300):
					velocity = 200;

				motors.move(velocity, velocity);
			else:
				#girar
				if(turn_degrees_needed > 0):
					print("Going to move left")
					motors.move(70, -70);
				else: 
					print("Going to move right")
					motors.move(-70, 70);
			#ir derecho;
			#recorrer 2 metros
			destiny = imu.get_degrees_and_distance_to_gps_coords(latitude2, longitud2);
			#time.sleep(1);


		motors.move(0,0);
		print("End thread Navigation");

def start():
	Imu.init();

	Camera.init();

	# Create new threads
	thread1 = LidarSocketThread(1, "LidarSocketThread");
	thread2 = MapThread(2, "MapThread");
	#thread3 = NavigationThread(3, "NavigationThread");

	# Start new Threads
	thread1.start();
	thread2.start();
	#thread3.start();
	#thread4.start();

	thread1.join();
	thread2.join();
	#thread3.join();
	#thread4.join();

	print ("Terminating Navigation");


'''
' Inicio del programa
'''
start();