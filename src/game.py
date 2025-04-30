from conf import *
from builder import *
from space import *
from bug import *
from engine import *
from tower import *


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
		self.particles = []
	
	def scale(self):
		return SUBDIVISION**(self.camera_level)

	def evolve(self,dt):

		self.builder.evolve(dt)
		self.builder.set_parent(self.get_current_space(self.builder))
		self.init_space_at_builder()

		for o in self.objects:
			if type(o) in [Bug]:
				o.evolve(dt)
			if type(o)==Bug:
				o.set_parent(self.get_current_space(o))
		
		target = self.builder.level-1
		self.camera_level = lerp_approach(self.camera_level,target,abs(self.camera_level-target),dt)
		self.camera = self.builder.r.copy()

		num_types = {}
		for o in self.objects:
			key = str(type(o))
			if key in num_types:
				num_types[key]+=1
			else:
				num_types[key]=1
		log("object-readout",str(num_types))

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
		if not space.is_free():
			return
		space.subdivide()
		for c in space.children:
			self.spaces.append(c)

	def place_object(self,o):
		space = self.get_current_space(self.builder)
		if not space:
			return False
		if not space.is_free():
			return False
		o.r = space.r.copy()
		o.set_parent(space)
		space.children.append(o)
		self.objects.append(o)
		return True

	def place_bug(self):
		b = Bug()
		if self.place_object(b):
			b.target = self.builder


	def place_engine(self):
		e = Engine()
		self.place_object(e)

	def place_tower(self):
		t = Tower()
		self.place_object(t)
		for o in self.objects:
			if isinstance(o,PoweredObject):
				t.connect(o)
		

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


	