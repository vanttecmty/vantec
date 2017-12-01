'''
	@desc 			Camera setup and configuration
	@author 		Marco Gil marcogil93@gmail.com
	@created_at 	2017-11-30 
	@updated_at 	2017-11-30 Restructuration and comments. 
'''

import datetime
import serial
import time
#import cv2
import cv2
import dbscan_contours as dbscan

leidoAnterior = ""

ID_COMPUTER_CAMERA = 0;
ID_EXTRERNAL_CAMERA = 1;

class Camera:
	def __init__(self):
		self.capture = None;
		self.frame = None;

		#set correct camera
		self.capture = cv2.VideoCapture(ID_EXTRERNAL_CAMERA);

		if(self.capture.isOpened() == False):
			sys.exit("No hay cámara");;

	def read(self, print_read = True):
		#Read camera
		self.frame = capture.read();
		#Print image

		if print_read:
			cv2.imshow('cam', self.frame[1]);
			cv2.waitKey(100);

	def getObstacles(self):
		#print read capture
		print_read = True
		self.read(print_read;

		#If camera read corectly
		if self.frame[0]:
			#get Camera obstacles
			values = dbscan.get_obstacles(frame[1],'yg', False);

			return values[1];
		else:
			return [];
