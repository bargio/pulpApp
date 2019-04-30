import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 5000                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)   # Now wait for client connection.
print(host)
print(port)
print(s)
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   c.sendall('Thank you for connecting'.encode())
   print (c.recv(1024).decode())
   c.close()