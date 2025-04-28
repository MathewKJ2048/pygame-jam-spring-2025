from conf import *
from builder import *


class Game:
	def __init__(self):
		self.time = 0
		self.spaces = []
		self.objects = []
		self.debug_transcript = {}
		self.running = True
		self.camera = Vector2(0,0)
		self.scale = 1
		self.builder = Builder()

	def evolve(self,dt):
		self.builder.evolve(dt)
		pass
	def log(self,key,value):
		self.debug_transcript[key] = value
	def exit(self):
		self.running = False

	