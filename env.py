import xmlrpc.client
import time
import grequests
import json
import time

class Auto_deployment_env():
	def __init__(self):
		# self.req_list = [   # 请求列表
		#     grequests.get('http://192.168.0.210:5001/face'),    
		#     grequests.get('http://192.168.0.210:5001/face'),    
		#     grequests.get('http://192.168.0.210:5001/face'),

		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),
		#     grequests.get('http://192.168.0.210:5002/iot'),

		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),
		#     grequests.get('http://192.168.0.210:5003/api'),]

		self.req_list = [
		'http://192.168.0.210:5001/face',
		'http://192.168.0.210:5001/face',
		'http://192.168.0.210:5001/face',

		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',
		'http://192.168.0.210:5002/iot',

		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		'http://192.168.0.210:5003/api',
		]

		self.state = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0]
		self.observaiton_space = 15

	def reset(self):
		with xmlrpc.client.ServerProxy("http://192.168.0.210:8001/") as proxy:
			reset = proxy.reset()
		self.state = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0]
		return [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0]

	def step(self, action):
		#take the action input
		next_state = self.calculate_next_state(action)

		#avoid case not avaiable node, means invalid operation
		if sum(next_state[0:4]) == 0 or sum(next_state[5:9]) == 0 or sum(next_state[10:14]) == 0:
			print("here")
			return self.state, 0.0, False

		if self.state == next_state:
			pass
		else:
			previous_sum = sum(self.state) 
			current_sum = sum(next_state)
			self.state = next_state
			#if update make some constraint is 0 and not scale yet, it will stuck here
			#which means, avoid the 0 case

			#add
			if previous_sum < current_sum:
				self.update()
				self.scale()
			else:
				#scale
				self.scale()
				self.update()

			time.sleep(1)

			# #scale
			# self.scale()

		#sleep to wait the service stable

		#call send function
		results = self.send()

		#calculate reward
		print("rewarding")
		face_reward = self.reward(results[0:2],10)
		iot_reward = self.reward(results[3:22],0.6)
		api_reward = self.reward(results[23:32],0.8)
		reward = (face_reward+iot_reward+api_reward)/3
		print(reward)

		#prepare done flag
		done = False
		if reward > 0.9:
			done = True
			reward = 10
		else:
			reward = reward -1
		return next_state, reward, done

	def send(self):
		print("sending")
		# res_list = grequests.map(self.req_list)    # 并行发送，等最后一个运行完后返回
		res_list = grequests.map(grequests.get(link, timeout=10.0) for link in self.req_list)
		print("received")
		return res_list

	def calculate_next_state(self, action):
		state = self.state
		next_state = []
		n = len(state)
		for i in range(0,n):
			value = state[i] + action[i]
			if value >= 1:
				value = 1
			else:
				value = 0
			next_state.append(value)

		return next_state

	def update(self):
		with xmlrpc.client.ServerProxy("http://192.168.0.210:8001/") as proxy:
			proxy.update(self.state)

	def reward(self, responses, k:int):
		n = float(len(responses))
		success = 0.0
		for r in responses:
			if r == None:
				continue
			else:
				v = eval(r.text)
				t = v['time']
				if t <= k:
					success +=1
		return (success/n)

	def scale(self):
		# face = max(sum(self.state[0:4]),1)
		# iot = max(sum(self.state[4:9]),1)
		# api = max(sum(self.state[10:14]),1)
		face = sum(self.state[0:4])
		iot = sum(self.state[4:9])
		api = sum(self.state[10:14])
		with xmlrpc.client.ServerProxy("http://192.168.0.210:8001/") as proxy:
			remain = proxy.scale([face,iot,api])
		return remain

if __name__ == "__main__":
	env = Auto_deployment_env()
	r = env.reset()
# 	# print(r)
# 	# env.step([-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0])
