import socket
import threading
import sys

class Server:
	sket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []

	def __init__(self):
		self.sket.bind( ('0.0.0.0', 10000) )
		self.sket.listen(1)

	def sendMessage(self, conn):
		while True:
			inp = input()
			if inp == "exit":
				conn.send(bytes("chat exit", 'utf-8'))
				conn.close()
				exit(0)
			conn.send(bytes(input(), 'utf-8'))

	'''def handle(self, conn, add):
		while True:
			data = conn.recv(1024)
			print(data)

			if not data:
				self.connections.remove(conn)
				conn.close()'''

	def run(self):
		while True:
			conn, add = self.sket.accept()
			if conn is not None:
				print("connected")
				conn.send(bytes("connected", 'utf-8'))
			'''self.connections.append(conn)
			conThread = threading.Thread(target=self.handle, args=(conn,add))
			conThread.daemon = True
			conThread.start()
			print(conn)'''
			iT = threading.Thread(target=self.sendMessage, args=(conn,))
			iT.daemon = True
			iT.start()

			while True:
				data = conn.recv(1024)
				print(str(data.decode('utf-8')))
				if not data:
					break

class Client:
	sket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def sendMessage(self):
		while True:
			inp = input()
			if inp == "exit":
				self.sket.send(bytes("chat exit", 'utf-8'))
				self.sket.close()
				exit(0)
			self.sket.send(bytes(inp, 'utf-8'))

	def __init__(self, add):
		self.sket.connect( (add, 10000) )

		iT = threading.Thread(target=self.sendMessage)
		iT.daemon = True
		iT.start()

		while True:
			data = self.sket.recv(1024)
			print(str(data.decode('utf-8')))
			if not data:
				break

if len(sys.argv) > 1 :
	c1 = Client(sys.argv[1])
	#c1.run()
else :
	s1 = Server()
	s1.run()
