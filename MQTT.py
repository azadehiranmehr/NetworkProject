import paho.mqtt.client as mqtt
import time
import datetime
import json
import threading
mbroker="localhost" #mosquitto
port =1883
# ssl_port=8883 #ssl
times = []
keepalive=1800
SSL_Connections=0 # how many SSL connections to establish
Normal_connections=300 # how many normal connections to establish
message_interval=0.01 #0.001
loops=2 #how many messsages to publish
verbose=False
message="The Quick Brown Fox"
topic="mbroker-test/test"
########
run_flag=True
readings={"max":0,"min":0,"avg":0,"count":0}
totals={"max":0,"min":0,"avg":0,"count":0}
def extract_time(msg):
   f=msg.find("X")
   count=int(msg[:f])
   msg=msg[f:]
   p=msg.find("Z")
   t=int(msg[6:p])

   return (t,count)


def on_log(client, userdata, level, buf):
   print(buf)
def on_message(client, userdata, message):
   #time.sleep(1)
   global messages_received
   msg=str(message.payload.decode("utf-8"))
   if verbose:
      print("topic ",message.topic," message received",msg)
   messages_received +=1
   t,count=extract_time(msg)
   time_taken=int((time.time()*1000)-t )
   #print("time taken =",time_taken," Milli seconds")
   if time_taken >readings["max"]:
      readings["max"]=time_taken
   if time_taken <readings["min"] or readings["min"]==0:
      if time_taken !=0:
         readings["min"]=time_taken
   avg=readings["avg"]+time_taken

   readings["avg"]=avg

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        count=userdata["count"]
        topic=userdata["topic"]
        if verbose:
           print("subscribing to topic",topic)
        client.subscribe(topic)
        #print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()  
def on_disconnect(client, userdata, rc):
   pass
   #print("client disconnected ok")
def on_publish(client, userdata, mid):
   # time.sleep(1)
   print("In on_pub callback mid= "  ,mid)
def check_messages():
   for i in range(nclients):
      if client.userdata["received_count"]==1:
         print("error client ",i)

def Create_connections(nclients,port,SSL_Flag=False):
   count=1
   for i in range(nclients):
      i+=1
      if SSL_Flag:
         cname ="python-ssl"+str(i)
      else:
         cname ="python-"+str(i)
      topic="mbroker-test/test"+str(i)
      userdata={"count":i,"topic":topic,"received_count":0}
      client = mqtt.Client(cname,userdata=userdata)             #create new instance
      if SSL_Flag:
         print("ok")
         # client.tls_set('/Users/imanbahmani/Documents/mbroker/mbroker.emqx.io-ca.crt',tls_version=2)
      try:
         client.connect(mbroker,port,keepalive)         #connect to mbroker 
         #client.on_log=on_log #this gives getailed logging
         client.on_connect = on_connect
         client.on_disconnect = on_disconnect
         #client.on_publish = on_publish
         client.on_message = on_message
         print("connecting client ",cname)
         clients.append(client)
         while not client.connected_flag:
            client.loop()
            # time.sleep(0.05)
      except:
      # except AssertionError as error:
         print("connection failed")
         # print(error)
         exit(1) #Should quit or raise flag to quit or retry

def multi_loop(nclients):
   global run_flag 
   while run_flag: 
      for i in range(nclients):
         client=clients[i]
         client.loop(0.01)

mqtt.Client.connected_flag=False#create flag in class
clients=[]
print("Creating Normal Connections ",Normal_connections," clients")
Create_connections(Normal_connections,port,False)
if SSL_Connections!=0:
   print("Creating SSL Connections ",SSL_Connections," clients")
   Create_connections(SSL_Connections,ssl_port,True)
nclients=len(clients)
t = threading.Thread(target=multi_loop,args=(nclients,)) #start multi loop
t.start()
print("All clients connected ")

#

print("Publishing ")
run_count=1
messages_received=0
try:
   while run_count<loops+1:
      count=1
      print("start run ",run_count)
      start_time=time.time()
      for client in clients:

         start_time_first=time.time()

         counter=str(count).rjust(6,"0")
         msg=counter+"XXXXXX"+str(int(time.time()*1000))+"ZZZZZZ"+"  "+ message
         #print(str(int(time.time()*1000)))
         if verbose:
            print("publish ",count)
         topic="mbroker-test/test"+str(count)
         client.publish(topic,msg)
         count+=1
         end_time_first=time.time()
         delay_first = float(end_time_first)-float(start_time_first)

         g = float("{:.6f}".format(delay_first)) 
         times.append(float(g))
         # time.sleep(message_interval)

      msg_rate=int((count-1)/(time.time()-start_time))
      print("message rate = ",msg_rate ,"messages per second")
      # time.sleep(5)
      # time.sleep(1)
      if messages_received !=count-1:
         print("error messages received "+ str(messages_received)," sent ",str(count-1))
      else:
         print("Successful Run messages received "+ str(messages_received),\
               " sent ",str(count-1))
         # print("Max time ",readings["max"]," ms")
         # print("Min time ",readings["min"]," ms")
         # print("Average time ",int(readings["avg"]/(count-1))," ms")

 
      readings={"max":0,"min":0,"avg":0,"count":0}
      messages_received=0
      run_count+=1
except KeyboardInterrupt:
   print("interrupted  by keyboard")
   run_flag=False

run_flag=False
for client in clients:
   client.disconnect()

time.sleep(5)
print("Finished -number of runs ",run_count-1)


print("Endssssssssssssssssssss")


print ('Average: {}'.format(sum(times) / (Normal_connections) if times else 0))
print ('Min: {}'.format(min(times)))
print ('Max: {}'.format(max(times)))



