from conf import *
from builder import *
from space import *
from bug import *
from engine import *
from tower import *
from battery import *
from warper import *
from cannon import *


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
		self.networks = []
	
	def scale(self):
		return SUBDIVISION**(self.camera_level)
	
	def exit(self):
		self.running = False

	def evolve_camera(self,dt):
		target = self.builder.level
		self.camera_level = lerp_approach(self.camera_level,target,abs(self.camera_level-target),dt)
		self.camera = self.builder.r.copy()

	def generate_log(self):
		num_types = {}
		for o in self.objects:
			key = str(type(o))
			if key in num_types:
				num_types[key]+=1
			else:
				num_types[key]=1
		log("object-readout",str(num_types))

	def evolve(self,dt):

		self.builder.evolve(dt)
		self.builder.set_parent(self.get_current_space(self.builder))
		self.init_space_at_builder()

		for o in self.objects:
			o.evolve(dt)
			if type(o)==Bug:
				o.set_parent(self.get_current_space(o))
		
		self.evolve_camera(dt)
		self.generate_log()

	

	def get_current_space(self,o):
		level = -1
		space = None
		for s in self.spaces:
			if s.contains(o) and s.level > level:
				space = s
				level = s.level
		return space

	def compute_networks(self):
		self.networks = []
		for o in self.objects:
			if not isinstance(o,PoweredObject):
				continue
			redundant = False
			for n in self.networks:
				if n.contains(o):
					redundant = True
					break
			if redundant:
				continue
			n = Network()
			n.objects = o.get_network_objects()
			self.networks.append(n)
			o.network = n

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

	def place_powered_object(self,o):
		self.place_object(o)
		self.make_connection(o)

	def remove_object(self,o):
		self.objects.remove(o)
		o.parent.children.remove(o)
	
	def remove_powered_object(self,o):
		self.remove_object(o)
		connected_objects = o.get_connected_objects()
		for c in connected_objects:
			c.disconnect(o)
			self.compute_networks()
		for c in connected_objects:
			self.make_connection(c)

	def remove_selected_object(self):
		space = self.get_current_space(self.builder)
		if not space:
			return False
		if space.is_free():
			return False
		selected_object = space.get_placed_objects()[0]
		if isinstance(selected_object,PoweredObject):
			self.remove_powered_object(selected_object)
		else:
			self.remove_object(selected_object)
		return True

		
	def make_connection(self,t):

		# get all suitable (in range, and not already transitively connected)
		powered_objects = [o for o in self.objects if isinstance(o,PoweredObject)]
		self.compute_networks()
		suitable = [o for o in powered_objects if o!=t and t.is_connectable(o) and t not in o.network.objects]

		# use network to form equivalence classes
		network_classes_unprocessed = [[s for s in suitable if n.contains(s)] for n in self.networks]
		network_classes = [n for n in network_classes_unprocessed if len(n) != 0]

		# in each equivalence class, pick the best one
		def pick_best(o, options): # assuming all options are viable:
			# if o has only one free port, the ones with just one free port are rejected
			if len(o.get_free_ports()) == 1:
				options = [op for op in options if len(op.get_free_ports())!=1]
			if len(options)==0:
				return None

			# same level is preferred
			# within same level, closest is preferred
			best_diff_in_levels = min([abs(o.level-op.level) for op in options]) # extract minimum level diff
			options = [op for op in options if abs(o.level-op.level) == best_diff_in_levels] # filter level
			options.sort(key=lambda op: (o.r-op.r).length()) # sort by size
			return options[0]

		# sort the equivalence classes by network size
		network_classes.sort(key=lambda n: -len(n[0].network.objects))

		# connect to each network, from largest to smallest
		for n in network_classes:
			best = pick_best(t,n)
			if not best:
				continue
			if best in t.network.objects: # no need to make cycles
				continue
			t.connect(best)
			self.compute_networks()
		return

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

	def expand(self):
		space = self.get_current_space(self.builder)
		if not space:
			return
		if not space.is_free():
			return
		space.subdivide()
		for c in space.children:
			self.spaces.append(c)

	def place_bug(self):
		b = Bug()
		if self.place_object(b):
			b.target = self.builder
	def place_engine(self):
		self.place_powered_object(Engine())
	def place_tower(self):
		self.place_powered_object(Tower())
	def place_high_tower(self):
		self.place_powered_object(HighTower())
	def place_battery(self):
		self.place_powered_object(Battery())
	def place_cannon(self):
		self.place_powered_object(Cannon())
	def place_warper(self):
		self.place_powered_object(Warper())


def process_pressed_keys(game):
	pressed_keys = pygame.key.get_pressed()
	game.builder.v = Vector2(0,0)
	if pressed_keys[pygame.K_LEFT]:
		game.builder.v+=-I
	if pressed_keys[pygame.K_RIGHT]:
		game.builder.v+=I
	if pressed_keys[pygame.K_UP]:
		game.builder.v+=J
	if pressed_keys[pygame.K_DOWN]:
		game.builder.v+=-J
	if game.builder.v.length() > 0:
		game.builder.v = game.builder.v.normalize()
	game.builder.v*=VELOCITY

def process_keydown_event(event,game):
	if event.key == pygame.K_s:
		game.expand()
	if event.key == pygame.K_b:
		game.place_bug()
	if event.key == pygame.K_e:
		game.place_engine()
	if event.key == pygame.K_t:
		game.place_tower()
	if event.key == pygame.K_h:
		game.place_high_tower()
	if event.key == pygame.K_v:
		game.place_battery()
	if event.key == pygame.K_w:
		game.place_warper()
	if event.key == pygame.K_c:
		game.place_cannon()
	if event.key == pygame.K_q:
		game.remove_selected_object()