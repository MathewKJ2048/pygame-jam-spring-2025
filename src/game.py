from conf import *

class Game:
	def __init__(self):
		self.time = 0
		self.spaces = []
		self.objects = []
		self.debug_transcript = {}
		self.running = True
	def update(self,dt):
		pass
	def log(self,key,value):
		self.debug_transcript[key] = value
	def exit(self):
		self.running = False

	