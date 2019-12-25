import socket
import cv2
import numpy as np

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#host = '192.168.0.100'
host = '127.0.0.1'
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(15)

for _ in range(4):
	client_sock, client_addr = sock.accept()
	filename = client_sock.recv(5)
	print(filename)
	while (True):
		tmp = client_sock.recv(16)
	
		if (tmp==b''):	# transmission done
			break
		img_size = int((tmp).decode('utf-8'))
		imgstr = recvall(client_sock, img_size)
		img = cv2.imdecode((np.fromstring(imgstr,dtype='uint8')),1)
		cv2.imshow('asdf', img)
		cv2.waitKey(1)

