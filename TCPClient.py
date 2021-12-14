from socket import *
import os
import time
ts = time.time()
import threading


def mt(i):
    print (i)
    time.sleep(1)


times = []
for x in range(300):
    # print(x)
    serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    sentence = str(ts)
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server Replay:', modifiedSentence.decode())
    print ('From Server Send:', sentence)
    delay = float(modifiedSentence.decode())-float(sentence)
    print(delay)
    times.append(float(delay))
    clientSocket.close()
    threadProcess = threading.Thread(name='simplethread', target=mt, args=[x])
    threadProcess.daemon = True
    threadProcess.start()
    
        
print ('Average: {}'.format(sum(times) / (300) if times else 0))
print ('Min: {}'.format(min(times)))
print ('Max: {}'.format(max(times)))
# # Import socket module
# import socket


# def Main():
# 	# local host IP '127.0.0.1'
# 	host = '127.0.0.1'

# 	# Define the port on which you want to connect
# 	port = 12345

# 	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 	# connect to server on local computer
# 	s.connect((host,port))

# 	# message you send to server
# 	message = "shaurya says geeksforgeeks"
# 	while True:

# 		# message sent to server
# 		s.send(message.encode('ascii'))

# 		# messaga received from server
# 		data = s.recv(1024)

# 		# print the received message
# 		# here it would be a reverse of sent message
# 		print('Received from the server :',str(data.decode('ascii')))

# 		# ask the client whether he wants to continue
# 		# ans = input('\nDo you want to continue(y/n) :')
# 		# if ans == 'y':
# 		# 	continue
# 		# else:
# 		# 	break
# 	# close the connection
# 	s.close()

# if __name__ == '__main__':
# 	Main()
