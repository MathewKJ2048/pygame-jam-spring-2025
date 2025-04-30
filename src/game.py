from conf import *
from builder import *
from space import *
from bug import *


class Game:
	def __init__(self):
		self.time = 0
		self.spaces = []
		self.objects = []
		self.running = True
		self.camera = Vector2(0,0)
		self.camera_angle = math.pi/6
		self.camera_level = 0
		self.builder = Builder()
	
	def scale(self):
		return SUBDIVISION**(self.camera_level)

	def evolve(self,dt):

		self.builder.evolve(dt)
		self.builder.set_parent(self.get_current_space(self.builder))
		self.init_space_at_builder()

		for o in self.objects:
			o.evolve(dt)
			if type(o)==Bug:
				o.set_parent(self.get_current_space(o))
		
		target = self.builder.level-1
		self.camera_level = lerp_approach(self.camera_level,target,abs(self.camera_level-target),dt)
		self.camera = self.builder.r.copy()
		log("game level",self.camera_level)

	def exit(self):
		self.running = False


	def get_current_space(self,o):
		level = -1
		space = None
		for s in self.spaces:
			if s.contains(o) and s.level > level:
				space = s
				level = s.level
		return space


	def expand(self):
		
		space = self.get_current_space(self.builder)
		if not space:
			return
		space.subdivide()
		for c in space.children:
			self.spaces.append(c)

	def place_bug(self):
		space = self.get_current_space(self.builder)
		if not space:
			return
		b = Bug()
		b.r = self.builder.r.copy()
		b.set_parent(space)
		b.target = self.builder
		self.objects.append(b)
		

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


	