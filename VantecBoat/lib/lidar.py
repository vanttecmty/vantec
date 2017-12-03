
# socket in order to communicate with the lidar
import socket

'''
	LIDAR CONSTANTS
'''
LIDAR_SOCKET_PORT 		 = 8894;
LIDAR_SOCKET_BUFFER_SIZE = 4000;

class Lidar:
	def __init__(self):
		#Init communication
		self.socket = socket.socket();
		self.socket.bind(("localhost", LIDAR_SOCKET_PORT));
		self.socket.listen(1);
		conn, addr = self.socket.accept();
		self.socket_connection = conn;
		self.socket_address = address;
		self.runProgram = True;
		self.obstacles = [];

	def run(self):
		while self.runProgram:
			#Fetch the data
			message = self.socket_connection.recv(LIDAR_SOCKET_BUFFER_SIZE);

			#Format lidar measurements
			if message == "quit":
				break;

			#Format lidar measurements
			strMeasures = message.decode('utf-8');
			arrMeasures = strMeasures.split(";");

			if(len(arrMeasures) > 0):
				self.obstacles = arrMeasures;
				self.obstacles.pop();

		#Terminate socket connection
		self.socket_connection.close();  
		self.socket.close();

	#Read lidar obstacles from socket
	def get_obstacles(self):
		#Fetch the data from the socket
		message = self.socket_connection.recv(LIDAR_SOCKET_BUFFER_SIZE);

		#Format lidar measurements
		if message == "quit":
			break;

		#Format lidar measurements
		strMeasures = message.decode('utf-8');
		arrMeasures = strMeasures.split(";");

		if(len(arrMeasures) > 0):
			self.obstacles = arrMeasures;
			self.obstacles.pop();
		else:
			self.obstacles = [];

		return self.obstacles;

	def terminate(self):
		#Terminate socket connection
		self.socket_connection.close();  
		self.socket.close();