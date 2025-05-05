from conf import *
from builder import *
from space import *
from bug import *
from engine import *
from tower import *
from battery import *
from warper import *
from cannon import *
from particle import *
from controls import *


class Game:
	def __init__(self): 
		self.time = 0
		self.spaces = []
		self.objects = []
		self.running = True
		self.camera = Vector2(0,0)
		self.camera_angle = 0
		self.camera_omega = 0
		self.camera_level = 0
		self.builder = Builder()
		self.particles = []
		self.networks = []
		self.particles = []
		self.paused = False
		self.minimap = True
		self.init_state()

	def init_state(self):
		for i in range(-2,3):
			for j in range(-2,3):
				s = Space()
				s.r = Vector2(i,j)
				self.spaces.append(s)
				if i == 0 and j == 0:
					e = Engine()
					e.r = s.r
					self.objects.append(e)
					s.children.append(e)
					e.set_parent(s)
				elif i == 1 and j == 0:
					t = Tower()
					t.r = s.r
					self.objects.append(t)
					s.children.append(t)
					t.set_parent(s)
					self.make_connection(t)

	
	def scale(self):
		return SUBDIVISION**(self.camera_level)
	
	def exit(self):
		self.running = False

	def evolve_camera(self,dt):
		target = self.builder.level
		self.camera_level = lerp_approach(self.camera_level,target,abs(self.camera_level-target),dt)
		self.camera = self.builder.r.copy()
		self.camera_angle+=self.camera_omega*dt

	def generate_log(self):
		num_types = {}
		for o in self.objects:
			key = str(type(o))
			if key in num_types:
				num_types[key]+=1
			else:
				num_types[key]=1
		log("object-readout",str(num_types))
		log("particles",len(self.particles))
		log("minimap",self.minimap)

	def update_position(self,o):
		if o.parent:
			if o in o.parent.children:
				o.parent.children.remove(o)
		s = self.get_current_space(o)
		o.set_parent(s)
		if s:
			s.children.append(o)

	def remove_bug_objects(self,b):
		s = self.get_current_space(b)
		if not s:
			return
		for t in s.children:
			if type(t) != Space and type(t) != Bug:
				t.health = 0

	

	def remove_unhealthy_objects(self):
		for o in self.objects:
			if isinstance(o,PlacedObject):
				if o.health<=0:
					self.remove_any_type_object(o)
					self.particles+=o.get_final_particles()

					play_sound(destruction_sound)

	def evolve(self,dt):
		if self.paused:
			return

		self.builder.evolve(dt)
		self.builder.set_parent(self.get_current_space(self.builder))
		self.init_space_at_builder()

		for o in self.spaces:
			o.evolve(dt)
		for o in self.objects:
			o.evolve(dt)
		for o in self.networks:
			o.evolve(dt)
		for o in self.particles:
			o.evolve(dt)

		bugs = [b for b in self.objects if isinstance(b,Bug)]
		warpers = [w for w in self.objects if isinstance(w,Warper)]
		cannons = [c for c in self.objects if isinstance(c,Cannon)]

		for b in bugs:
			self.update_position(b)
			b.set_target(self.objects,backup_target=self.builder)
			self.remove_bug_objects(b)
		for c in cannons:
			c.set_target(self.objects)
		for w in warpers:
			self.operate_warper(w)

		self.remove_unhealthy_objects()

		self.evolve_camera(dt)
		self.generate_log()

		for o in self.objects:
			if o.parent:
				if o not in o.parent.children:
					log("error "+str(type(o)))
					o.parent.children.append(o)

		print(self.objects)
		for o in self.objects:
			self.particles+=o.make_particles()
		self.particles+=self.builder.make_particles()

		for p in self.particles:
			if p.time > p.max_time:
				self.particles.remove(p)
		
		



	

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
		play_sound(construction_sound)
		return True

	def place_powered_object(self,o):
		self.place_object(o)
		self.make_connection(o)

	def remove_object(self,o):
		if o in self.objects:
			self.objects.remove(o)
		if o.parent:
			if o in o.parent.children:
				o.parent.children.remove(o)
	
	def remove_powered_object(self,o):
		self.remove_object(o)
		connected_objects = o.get_connected_objects()
		for c in connected_objects:
			c.disconnect(o)
			self.compute_networks()
		for c in connected_objects:
			self.make_connection(c)
	
	def remove_children_of_warper(self,w):
		spaces_inside = [o for o in w.parent.children if type(o) == Space]
		# remove all placed objects
		for s in spaces_inside:
			for o in s.children:
				if isinstance(o,PlacedObject):
					self.remove_any_type_object(o)
		# remove spaces
		self.remove_spaces_in_warper(w)
		

	def remove_spaces_in_warper(self,w):
		parent_space = w.parent
		spaces_inside = parent_space.get_space_descendants()
		for s in spaces_inside:
			self.spaces.remove(s)
			if s in parent_space.children:
				parent_space.children.remove(s)

	def remove_warper(self,w):
		self.remove_children_of_warper(w)
		self.remove_powered_object(w)
	
	def remove_any_type_object(self,o):
		if isinstance(o,Warper):
			self.remove_warper(o)
		if isinstance(o,PoweredObject):
			self.remove_powered_object(o)
		else:
			self.remove_object(o)


	def remove_selected_object(self):
		space = self.get_current_space(self.builder)
		if not space:
			return False
		possible = [t for t in space.get_placed_objects() if not isinstance(t,Bug)]
		if len(possible)==0:
			return False
		self.remove_any_type_object(possible[0])
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
		self.subdivide_space(space)

	def subdivide_space(self,space):
		space.subdivide()
		for c in space.children:
			if type(c) == Space:
				self.spaces.append(c)

	

	def operate_warper(self,w):
		space = w.parent
		if not space:
			return
		if w.is_full() and not space.is_divided():
			self.subdivide_space(space)
			play_sound(warp_sound)
		if w.is_empty() and space.is_divided():
			self.remove_children_of_warper(w)
			play_sound(warp_sound)


	def place_bug(self):
		b = random.choice([nimble(),normal(),tank()])
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



	