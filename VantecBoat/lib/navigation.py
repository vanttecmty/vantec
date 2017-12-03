'''
	@name       	navigation.py
    @desc 			Navigation file. integration of boat movement 
	@author 		Marcopolo Gil Melchor marcogil93@gmail.com
	@created_at 	2017-11-28 
	@updated_at 	2017-11-28
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

class Navigation:
	def __init__(self):
		frame = None;

	'''
	@desc 	set the obstacles in the map
	@params lidar obstacles, camera obstacles
	@return matrix Map
	'''
	def update_destiny():
		self.distance = distance;
		self.degree = degree;
		self.stopNavigation = False;

	def navigate(self):
		lastOrientationDegree = 0;
		turn_degrees_needed   = 0;
		turn_degrees_accum    = 0;
		
		imu = Imu();
		#clean angle;
		imu.get_delta_theta();

		#Condition distance more than 2 meters. 
		while distance > 2 and self.stopNavigation != False:
			#print("degrees: ", imu.NORTH_YAW);
			#print("coords: ", imu.get_gps_coords());
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
				imu_angle = imu_angle - 360;
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