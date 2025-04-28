from conf import *
from builder import *
from space import *


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
		self.init_space_at_builder()
		pass
	def log(self,key,value):
		self.debug_transcript[key] = value
	def exit(self):
		self.running = False

	def builder_in_space(self):
		for s in self.spaces:
			if s.contains(self.builder):
				return True
		return False
	def init_space_at_builder(self):
		if self.builder_in_space():
			return False
		r = self.builder.r
		r_ = Vector2(round(r.x),round(r.y))
		space = Space()
		space.r = r_
		self.spaces.append(space)


	