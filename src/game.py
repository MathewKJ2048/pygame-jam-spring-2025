from conf import *
from builder import *
from space import *


class Game:
	def __init__(self):
		self.time = 0
		self.spaces = []
		self.objects = []
		self.running = True
		self.camera = Vector2(0,0)
		self.scale = 1
		self.builder = Builder()

	def evolve(self,dt):
		self.builder.evolve(dt)
		self.builder.parent = self.get_current_space()
		self.init_space_at_builder()
		pass
	def exit(self):
		self.running = False


	def get_current_space(self):
		level = -1
		space = None
		for s in self.spaces:
			if s.contains(self.builder) and s.level > level:
				space = s
				level = s.level
		return space


	def expand(self):
		
		space = self.get_current_space()
		if not space:
			return
		space.subdivide()
		for c in space.children:
			self.spaces.append(c)
		

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


	