import os  
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy 
import sys
import json
import os
from multiprocessing.dummy import Pool as ThreadPool
import docker


class Node:
    def __init__(self, port):
        self.port = port
        self.start = "docker node update "
        self.hostname = ["4gb01","2gb01","1gb02","1gb01","pi3"]
        self.services = ["face","iot","api"]
        # self.client = docker.from_env()
        # self.services_objects = ["","",""]
        # self.services_objects_init()

        # self.face = self.client.services.get("ow4r53cbcytt") 
        # self.iot = self.client.services.get("k3idewx9z4um") 
        # self.api = self.client.services.get("zn48f0vsm3dh") 

    def reset(self):
        print("reset")
        os.system("docker node update --label-add face=true 4gb01")
        os.system("docker node update --label-add iot=true 4gb01")
        os.system("docker node update --label-add api=true 4gb01")

        os.system("docker node update --label-add face=false 2gb01")
        os.system("docker node update --label-add iot=false 2gb01")
        os.system("docker node update --label-add api=false 2gb01")

        os.system("docker node update --label-add face=false 1gb02")
        os.system("docker node update --label-add iot=false 1gb02")
        os.system("docker node update --label-add api=false 1gb02")

        os.system("docker node update --label-add face=false 1gb01")
        os.system("docker node update --label-add iot=false 1gb01")
        os.system("docker node update --label-add api=false 1gb01")

        os.system("docker node update --label-add face=false pi3")
        os.system("docker node update --label-add iot=false pi3")
        os.system("docker node update --label-add api=false pi3")

        self.scale([1,1,1])
        print("done")
        return "done"

  #   def update(self, state = []):
  #   	face = state[0:4]
		# iot = state[5:9]
		# api = state[10:14]

		# for i in range 


    def update(self, state=[]):
    	print(len(state))
    	print(state)
    	face = state[0:5]
    	print(face)
    	iot = state[5:10]
    	print(iot)
    	api = state[10:15]
    	print(api)

    	for i in range(0,len(face)):
    		print(len(face))
    		print(i)
    		string = ""
    		if face[i] == 1:
    			string = "--label-add face=true " + self.hostname[i]
    		else:
    			string = "--label-add face=false " + self.hostname[i]
    		command = self.start + string
    		print(command)
    		os.system(command)
    	
    	# if sum(face) == 0:
    		# os.system("docker node update --label-add face=true 4gb01")

    	for i in range(0,len(iot)):
    		string = ""
    		if iot[i] == 1:
    			string = "--label-add iot=true " + self.hostname[i]
    		else:
    			string = "--label-add iot=false " + self.hostname[i]
    		command = self.start + string
    		print(command)
    		os.system(command)

    	# if sum(iot) == 0:
    	# 	os.system("docker node update --label-add iot=true 4gb01")

    	for i in range(0,len(api)):
    		string = ""
    		if api[i] == 1:
    			string = "--label-add api=true " + self.hostname[i]
    		else:
    			string = "--label-add api=false " + self.hostname[i]
    		command = self.start + string
    		print(command)
    		os.system(command)

    	# if sum(api) == 0:
    	# 	os.system("docker node update --label-add api=true 4gb01")

    def scale(self,replicas=[]):
    	pool = ThreadPool()
    	inputs = [[0,replicas[0]],[1,replicas[1]],[2,replicas[2]]]
    	pool.map(self.scale_one,inputs)
    	pool.close()
    	pool.join()
    	return "done"

    def scale_one(self, inputs=[]):
    	service_name = self.services[inputs[0]]
    	replicas = inputs[1]
    	#just do the client.service update here
    	# service = self.services_objects[inputs[0]]
    	# print(service.name)
    	# print(replicas)
    	# service.scale(replicas)
    	command = "docker service scale "+service_name+"="+ str(replicas)
    	os.system(command)
    	print(command)

    # def services_objects_init(self):
    # 	services = self.client.services.list()
    # 	print(services)
    # 	for s in services:
    # 		if s.name == "face":
    # 			self.services_objects[0] = s
    # 		elif s.name == "iot":
    # 			self.services_objects[1] = s
    # 		elif s.name == "api":
    # 			self.services_objects[2] = s
    	# print(self.services_objects[0].name)

    def _start(self):
        s = SimpleXMLRPCServer(("0.0.0.0", self.port), allow_none = True)
        s.register_instance(self)
        print("server started")
        s.serve_forever()

if __name__ == "__main__":
    port = 8001
    node = Node(port)
    node._start()