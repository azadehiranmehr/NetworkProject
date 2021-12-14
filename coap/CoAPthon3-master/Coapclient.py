# -*- coding: utf-8 -*-

from queue import Queue
import random
import socket
import threading
import unittest
import time
from coapclient import HelperClient
from coapserver import CoAPServer
from coapthon import defines
from coapthon.messages.message import Message
from coapthon.messages.option import Option
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.serializer import Serializer


times = []
numberLoop = 300
ts = time.time()
__author__ = '....'
__version__ = "2.0"

PAYLOAD = "Lorem i"


def mt(i):
    print (i)
    time.sleep(1)
        
class Tests(unittest.TestCase):

    def setUp(self):
        self.server_address = ("127.0.0.1", 5683)
        self.current_mid = random.randint(1, 1000)
        self.server_mid = random.randint(1000, 2000)
        self.server = CoAPServer("127.0.0.1", 5683)
        self.server_thread = threading.Thread(target=self.server.listen, args=(1,))
        self.server_thread.start()
        self.queue = Queue()

    def tearDown(self):
        self.server.close()
        self.server_thread.join(timeout=25)
        self.server = None

    def _test_with_client(self, message_list):  # pragma: no cover
        client = HelperClient(self.server_address)
        for message, expected in message_list:
            if message is not None:
                received_message = client.send_request(message)
            if expected is not None:

                if expected.type is not None:
                    self.assertEqual(received_message.type, expected.type)
                if expected.mid is not None:
                    self.assertEqual(received_message.mid, expected.mid)
                self.assertEqual(received_message.code, expected.code)
                if expected.source is not None:
                    self.assertEqual(received_message.source, self.server_address)
                if expected.token is not None:
                    self.assertEqual(received_message.token, expected.token)
                if expected.payload is not None:
                    self.assertEqual(received_message.payload, expected.payload)
                if expected.options:
                    self.assertEqual(len(received_message.options), len(expected.options))
                    for o in expected.options:
                        assert isinstance(o, Option)
                        option_value = getattr(expected, o.name.lower().replace("-", "_"))
                        option_value_rec = getattr(received_message, o.name.lower().replace("-", "_"))
                        self.assertEqual(option_value, option_value_rec)
        client.stop()

    def _test_with_client_observe(self, message_list):  # pragma: no cover
        client = HelperClient(self.server_address)
        for message, expected in message_list:
            if message is not None:
                client.send_request(message, self.client_callback)
            if expected is not None:
                received_message = self.queue.get()
                if expected.type is not None:
                    self.assertEqual(received_message.type, expected.type)
                if expected.mid is not None:
                    self.assertEqual(received_message.mid, expected.mid)
                self.assertEqual(received_message.code, expected.code)
                if expected.source is not None:
                    self.assertEqual(received_message.source, self.server_address)
                if expected.token is not None:
                    self.assertEqual(received_message.token, expected.token)
                if expected.payload is not None:
                    self.assertEqual(received_message.payload, expected.payload)
                if expected.options:
                    self.assertEqual(len(received_message.options), len(expected.options))
                    for o in expected.options:
                        assert isinstance(o, Option)
                        option_value = getattr(expected, o.name.lower().replace("-", "_"))
                        option_value_rec = getattr(received_message, o.name.lower().replace("-", "_"))
                        self.assertEqual(option_value, option_value_rec)
        client.stop()

    def client_callback(self, response):
        print("Callback")
        self.queue.put(response)

    def _test_plugtest(self, message_list):  # pragma: no cover
        serializer = Serializer()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for message, expected in message_list:
            if message is not None:
                datagram = serializer.serialize(message)
                sock.sendto(datagram, message.destination)
            if expected is not None:
                datagram, source = sock.recvfrom(4096)
                received_message = serializer.deserialize(datagram, source)
                if expected.type is not None:
                    self.assertEqual(received_message.type, expected.type)
                if expected.mid is not None:
                    self.assertEqual(received_message.mid, expected.mid)
                self.assertEqual(received_message.code, expected.code)
                if expected.source is not None:
                    self.assertEqual(received_message.source, source)
                if expected.token is not None:
                    self.assertEqual(received_message.token, expected.token)
                if expected.payload is not None:
                    self.assertEqual(received_message.payload, expected.payload)
                if expected.options is not None:
                    self.assertEqual(received_message.options, expected.options)
                    for o in expected.options:
                        assert isinstance(o, Option)
                        option_value = getattr(expected, o.name.lower().replace("-", "_"))
                        option_value_rec = getattr(received_message, o.name.lower().replace("-", "_"))
                        self.assertEqual(option_value, option_value_rec)
        sock.close()

    def _test_datagram(self, message_list):  # pragma: no cover
        serializer = Serializer()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for message, expected in message_list:
            if message is not None:
                datagram, destination = message
                sock.sendto(datagram, destination)
            if expected is not None:
                datagram, source = sock.recvfrom(4096)
                received_message = serializer.deserialize(datagram, source)
                if expected.type is not None:
                    self.assertEqual(received_message.type, expected.type)
                if expected.mid is not None:
                    self.assertEqual(received_message.mid, expected.mid)
                self.assertEqual(received_message.code, expected.code)
                if expected.source is not None:
                    self.assertEqual(received_message.source, source)
                if expected.token is not None:
                    self.assertEqual(received_message.token, expected.token)
                if expected.payload is not None:
                    self.assertEqual(received_message.payload, expected.payload)
                if expected.options is not None:
                    self.assertEqual(received_message.options, expected.options)
                    for o in expected.options:
                        assert isinstance(o, Option)
                        option_value = getattr(expected, o.name.lower().replace("-", "_"))
                        option_value_rec = getattr(received_message, o.name.lower().replace("-", "_"))
                        self.assertEqual(option_value, option_value_rec)
        sock.close()
    
    def test_post(self):
        for x in range(numberLoop):
            print(x)
            
            print("TEST_POST")
            path = "/storage/new_res?id=1"

            ts = time.time()
            sentence = str(ts)

            req = Request()
            req.code = defines.Codes.POST.number
            req.uri_path = path
            req.type = defines.Types["CON"]
            req._mid = self.current_mid
            req.destination = self.server_address
            req.payload = "test"
            req.add_if_none_match()

            expected = Response()
            expected.type = defines.Types["ACK"]
            expected._mid = self.current_mid
            expected.code = defines.Codes.CREATED.number
            expected.token = None
            expected.payload = None
            expected.location_path = "storage/new_res"
            expected.location_query = "id=1"
            


            exchange1 = (req, expected)
            self.current_mid += 1

            self._test_with_client([exchange1])
            modifiedSentence = time.time()

            print("code"+str(expected.code))
            print("payload"+str(expected.payload))
            print("exchange1"+str(exchange1))
            

            print ('From Server Replay:', modifiedSentence)
            print ('From Server Send:', sentence)
            delay = float(modifiedSentence)-float(sentence)
            print(delay)
            times.append(float(delay))
            
            threadProcess = threading.Thread(name='simplethread', target=mt, args=[x])
            threadProcess.daemon = True
            threadProcess.start()
        
        print ('Average: {}'.format(sum(times) / (numberLoop) if times else 0))
        print ('Min: {}'.format(min(times)))
        print ('Max: {}'.format(max(times)))





if __name__ == '__main__':
      unittest.main()

