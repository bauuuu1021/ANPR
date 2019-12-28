import socket
import cv2
import numpy as np
from hdfs import InsecureClient

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

host = '0.0.0.0'
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(15)

for _ in range(5):
    client_sock, client_addr = sock.accept()
    filename = client_sock.recv(6)
    print(filename)
    export_video = cv2.VideoWriter(filename.decode('utf-8'),cv2.VideoWriter_fourcc(*'mp4v'), 60, (1280,720))
    while (True):
        # recv from stream client
        tmp = client_sock.recv(16)
        if (tmp==b''):	# transmission done
            break

        img_size = int((tmp).decode('utf-8'))
        imgstr = recvall(client_sock, img_size)  
        img = cv2.imdecode((np.fromstring(imgstr,dtype='uint8')),1)

        # img to video
        export_video.write(img)
    export_video.release()

    client = InsecureClient('http://master:9870', user='ubuntu')
    client.upload('/user/ubuntu', filename.decode('utf-8'), True)

