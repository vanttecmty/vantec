'''
	@desc 			Xbee Boat Communication
	@author 		Juan Carlos Aguilera aguilerapjc@gmail.com
	@created_at 	2017-06-05 
	@updated_at 	2017-11-28 Restructuration and comments. 
'''

import datetime
import serial
import time

leidoAnterior = ""

class Xbee:
	def __init__(self, portUSB):

		self.connection = serial.Serial(portUSB, 9600)
		self.timestamp = ''

	def send_to_station(self, meesage):
		date  = str(datetime.datetime.now());
		fecha = date.split('-');
		dia   = fecha[2].split(' ')[0];
		horas = fecha[2].split(' ')[1].split(':');
		self.timestamp = fecha[0] + fecha[1] + dia + horas[0] + horas[1] + horas[2][:2];

		#TODO checar el response para saber si mandó
		self.connection.write(bytes(self.timestamp + ',' + message + ','+'%', encoding='utf-8'));

	def send_to_boat(self, message):
		string = ',' + message + ',' + '%';

		#TODO checar el response para saber si mandó
		self.connection.write(bytes(string, encoding='utf-8'))

	def receive_from_station(self):
		leido = self.connection.read(17).decode("utf-8")
		data  = leido.split(',');
		data  = data[1 :];
		data  = data[: 6];

		return data;

	def receive_from_boat(self):
		leido=self.connection.read(47).decode("utf-8");

		return leido;

