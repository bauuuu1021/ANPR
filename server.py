import socket
import cv2
import numpy as np
from hdfs import InsecureClient
#from detect import *
from LicensePlateRec import *

host = '0.0.0.0'
port = 12345
client_num = 5

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def main():
    # socket initial setting
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(client_num)

    for _ in range(client_num):
        client_sock, client_addr = sock.accept()
        filename = client_sock.recv(6)
        print(filename)

        frame_num = 0
        result_txt = (filename.decode('utf-8')).split('.', 1)
        detect_result = open(result_txt[0]+'.txt', 'w')
        export_video = cv2.VideoWriter(filename.decode('utf-8'),cv2.VideoWriter_fourcc(*'mp4v'), 60, (1280,720))
        while (True):
            # recv from stream client
            tmp = client_sock.recv(16)
            if (tmp==b''):	# transmission done
                break
            
            # decode image
            img_size = int((tmp).decode('utf-8'))
            imgstr = recvall(client_sock, img_size)  
            img = cv2.imdecode((np.fromstring(imgstr,dtype='uint8')),1)

            
            # license plate detection
            if (detect(img) == True):
                detect_result.write(str(frame_num)+'\n') 
            
            # img to video
            export_video.write(img)
            
            frame_num += 1
        detect_result.close()
        export_video.release()

        
        # upload to HDFS
        client = InsecureClient('http://master:9870', user='ubuntu')
        client.upload('/user/ubuntu', filename.decode('utf-8'), True)
        client.upload('/user/ubuntu', result_txt[0]+'.txt', True)
        
if __name__ == '__main__':
    main()
