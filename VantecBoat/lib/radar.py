'''
	@name       	main.py
    @desc 			Navigation file. Definition and execution of threads and manipulation of components. 
    				Radar is set in centimeters resolution due tu objects size. 
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

#Basic libraries
import math

#N-dimensional array object for images, radar drawing
import numpy as np

#opencv
import cv2

#For image manipulations
from scipy import misc
from scipy.ndimage import rotate

import pathfindingv2 as pathfinding

#Set radar width and Height
MAP_WIDTH       = 1000;
MAP_HEIGHT      = 1000;
PIXELS_TO_CENTIMETER_RATIO = 2;
BOUY_RADIOUS    = 6;
BOAT_HEIGHT     = 58;
BOAT_WIDTH      = 34;
BOAT_X1         = int(MAP_WIDTH/2 - BOAT_WIDTH/2);
BOAT_Y1         = int(MAP_HEIGHT/2 - BOAT_HEIGHT/2);
BOAT_X2         = int(MAP_WIDTH/2 + BOAT_WIDTH/2);
BOAT_Y2         = int(MAP_HEIGHT/2 + BOAT_HEIGHT/2);
LIDAR_COORD_X   = 100;
LIDAR_COORD_Y   = int(100 - BOAT_HEIGHT / 2);#200

class Radar:
	def __init__(self):
		frame = None;
		emptyMap = self.new_map(MAP_WIDTH, MAP_HEIGHT);

	'''
	@desc 	set the obstacles in the map
	@params lidar obstacles, camera obstacles
	@return matrix Map
	'''
	def set_obstacles(self, lidarObstacles, cameraObstacles):
		#Set lidar Obstacles
		for measure in LlidarObstacles:
			data = measure.split(",");

			#get degree and distance (mm)
			degree = int(data[0]);
			distance = int(data[1]);

			#add front to right degrees (0-90)
			#add front to left degrees (270-360)
			if (degree > 0 and degree < 90) or (degree > 270 and degree < 360):
				#locate obstacles by the corresponding pixels
				#get x,y components from vector
				# distance must be converted to centimeters 
				#
				pixelX = LIDAR_COORD_X + int(math.cos(math.radians(degree - 90)) * float(distance / 10) / PIXELS_TO_CENTIMETER_RATIO);
				pixelY = LIDAR_COORD_Y + int(math.sin(math.radians(degree - 90)) * float(distance / 10) / PIXELS_TO_CENTIMETER_RATIO);
				#print(pixelX, pixelY);

				# expand the obstacle to boat size in white color
				cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);

				# set the exact coordinates of read obstacles
				cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);


		#Set Camera obstacles
		for obstacle in camObstacles:
			#obstacle is an array of form: [distance, degree]
			# distance is given by centimeters
			pixelX = LIDAR_COORD_X + int (math.cos(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / PIXELS_TO_CENTIMETER_RATIO);
			pixelY = LIDAR_COORD_Y + int (math.sin(math.radians(obstacle[1] - 90)) * float(obstacle[0]) / PIXELS_TO_CENTIMETER_RATIO);

			# expand the obstacle to boat size in white color
			cv2.circle(routeMap, (pixelX, pixelY), int(BOUY_RADIOUS + BOAT_WIDTH * 0.8), (255, 255 , 255), -1, 8);

			# set the exact coordinates of read obstacles
			cv2.circle(routeMap, (pixelX, pixelY), BOUY_RADIOUS, (0, 0, 255), -1, 8);
			pass;

		#draw boat
		#self.draw_boat(routeMap);

		#show image	
		#cv2.imshow('Route', routeMap);
		cv2.waitKey(100);

		return routeMap;

	'''
	@desc 	get the destiny pixel in our radar
	@params degree, 
			distance meters
	@return array pixels
	'''
	def get_destiny_pixel(degree, distance):
		#if distance is less than 8 meters away.
		# locate to exact pixel
		if(distance < 8):
			#escalar medidad de metros a centimetro -> multiplicar entre 100 
			destinyPixelX = LIDAR_COORD_X + int (math.cos(math.radians(degree + 90)) * float(distance * 100) / PIXELS_TO_CENTIMETER_RATIO);
			destinyPixelY = LIDAR_COORD_Y + int (math.sin(math.radians(degree + 90)) * float(distance * 100) / PIXELS_TO_CENTIMETER_RATIO);
			destinyPixel = [destinyPixelY, destinyPixelX];

		#elselocate partial destiny pixel.
		else:
			#locate destiny in top border.
			if(math.fabs(degree) < 45):
				destinyDistanceY = MAP_HEIGHT/2;
				destinyPixelY    = 0;
				destinyDistanceX = destinyDistanceY / math.tan(math.radians(degree + 90));
				destinyPixelX    = int(MAP_WIDTH/2 + destinyDistanceX);
				destinyPixel     = [destinyPixelY, destinyPixelX];

			#locate destiny in right border
			elif(degree < -45 and  degree > -135):
				destinyDistanceX = MAP_HEIGHT/2;
				destinyPixelX    = MAP_WIDTH - 1;
				destinyDistanceY = math.tan(math.radians(degree + 90)) * destinyDistanceX;
				destinyPixelY    = int(MAP_WIDTH/2 - destinyDistanceY);
				destinyPixel     = [destinyPixelY, destinyPixelX];

			#locate destiny in left border
			elif(degree > 45 and  degree < 135):
				destinyDistanceX = MAP_HEIGHT/2;
				destinyPixelX    = 0;
				destinyDistanceY = math.tan(math.radians(degree + 90)) * destinyDistanceX;
				destinyPixelY    = int(MAP_WIDTH/2 + destinyDistanceY);
				destinyPixel     = [destinyPixelY, destinyPixelX];

			#locate destiny in bottom border
			elif(math.fabs(degree) > 135):
				destinyDistanceY = MAP_HEIGHT/2;
				destinyPixelY    = MAP_HEIGHT - 1;
				destinyDistanceX = destinyDistanceY / math.tan(math.radians(degree + 90));
				destinyPixelX    = int(MAP_WIDTH/2 + destinyDistanceX);
				destinyPixel     = [destinyPixelY, destinyPixelX];
		
		return destinyPixel;

'''
	@desc 	get the boat front pixel
	@params None,
	@return pixel
	'''
	def get_boat_pixel():
		return [MAP_HEIGHT/2, MAP_WIDTH/2];
	'''
	@desc 	set the destiny pixel in our radar
	@params matrix map, destinyPixelY, destinyPixelX
	@return matrix Map
	'''
	def set_route(routeMap, destinyPixelY, destinyPixelX):
		destinyPixel = [destinyPixelY, destinyPixelX];
		#cv2.imshow('Route', routeMap);
		#cv2.waitKey(100);
		#cv2.imwrite('route_test.png',routeMap)
		#Todo: check if destiny is inside obstacle;

		#get rout points
		routePoints = pathfinding.a_star([int(MAP_WIDTH/2), int(MAP_HEIGHT/2)], destinyPixel, routeMap);
		routeLength = len(routePoints);

		for point in routePoints:
			routeMap[point[0]][point[1]] = [0, 0, 255];
			pass;

		# Check resolution PIXELS_TO_CENTIMETER_RATIO, if equals 2 then update each 50 cm
		if(routeLength > 100):
			pixelX = routePoints[-100][1];
			pixelY = routePoints[-100][0];
			degree = math.atan2(MAP_HEIGHT / 2 - pixelY, pixelX - MAP_WIDTH / 2);
		else: 
			degree = 0;

		return {
			'mapa': routeMap,
			'partial_degree': degree
		};

	'''
	@desc 	draw route on radar
	@params matrix map
	@return None
	'''
	def draw_radar(routeMap):
		self.draw_boat(routeMap);
		cv2.imshow('Route', routeMap);
		cv2.waitKey(100);

	def new_map(self, rows, cols):
		mapa = np.full((rows, cols, 3),0, dtype = np.uint8);
		return mapa;

	def draw_boat(self, mapa):
		cv2.rectangle(mapa,(BOAT_X1, BOAT_Y1),(BOAT_X2, BOAT_Y2), (0,255,0), 1, 8);