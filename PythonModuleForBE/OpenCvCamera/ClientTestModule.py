import socket

s = socket.socket()
port = 5000
s.connect(('10.41.13.51', port))
z = 'Your string'
print(s.recv(1024).decode())
s.sendall(z.encode())
s.close()
