from conf import *
from particle import *

class GameObject:
	def __init__(self,parent=None):
		self.r = Vector2(0,0)
		self.set_parent(parent)
		self.time = 0
		self.last_emitted_particle_time = -10
	def make_particles(self):
		if self.time - self.last_emitted_particle_time > 0.01:
			self.last_emitted_particle_time = self.time
			return self.get_particles()
	def get_particles(self):
		return []# explosion(1,self.r,1,0.5,K3,0.1)
	def get_final_particles(self):
		return explosion(self.get_render_size(),1000,Vector3(*self.r,1/2),5,2,K3-K3,0.1,darken(self.get_color(),0.1))
	def evolve(self,dt):
		self.time+=dt
	def size(self):
		return SUBDIVISION**(-self.level)
	def get_render_size(self):
		return self.size()
	def set_parent(self,parent):
		if parent:
			self.parent = parent
			self.level = parent.level+1
		else:
			self.parent = None
			self.level = 0
	def get_lines(self):
		return [(I3/2,-I3/2),(J3/2,-J3/2),(I3-I3,K3)]
	def get_color(self):
		return WHITE
	def get_width(self):
		return 2
	def get_animated_lines(self):
		f = min(self.time,1) # f is 0 initially, linearly grows to 1 then remains at 1
		if f == 1:
			return self.get_lines()
		def process(pp):
			p, q = pp
			mid = (p+q)/2
			p_, q_ = p-mid, q-mid
			return (mid+p_*f,mid+q_*f)
		l = self.get_lines()
		return [process(pp) for pp in l]

class PlacedObject(GameObject):
	MAX_HEALTH = 1
	def __init__(self):
		super().__init__()
		self.health = type(self).MAX_HEALTH

	def set_parent(self,parent):
		if parent:
			self.parent = parent
			self.level = parent.level
		else:
			self.parent = None
			self.level = 0

	def cause_damage(self,amount):
		self.health-=amount
		if self.health<0:
			self.health = 0

class MovingObject(PlacedObject):
	def __init__(self):
		super().__init__()
		self.render_level = self.level
		self.v = I
	def evolve(self,dt):
		super().evolve(dt)
		self.r+=self.v*self.size()*dt
		self.render_level = lerp_approach(self.render_level,self.level,1,dt)
	def get_render_size(self):
		return SUBDIVISION**(-self.render_level)
	

class Network:
	def __init__(self):
		self.objects = []
	def get_total_energy(self):
		return sum([o.stored for o in self.objects])
		
	def get_net_rate(self):
		return self.get_total_production_rate() - self.get_total_consumption_rate()

	def get_total_production_rate(self):
		return sum([o.production_rate for o in self.objects])

	def get_total_consumption_rate(self):
		return sum([o.consumption_rate for o in self.objects])
		
	def contains(self,o):
		return o in self.objects
	
	def evolve(self,dt):
		dE = self.get_net_rate()*dt
		# if energy is in shortfall, draw the energy from every node of the network
		# if energy is in excess, add to every node of the network, if they have capacity
		relevant_objects = [o for o in self.objects if (dE>0 and not o.is_full()) or (dE<0 and not o.is_empty())]
		if len(relevant_objects)==0:
			return
		dEn = dE/len(relevant_objects)
		for o in relevant_objects:
			o.flow(dEn)
		pass


class Port:
	def __init__(self,parent,r):
		self.parent = parent
		self.r = r # position of port relative to parent
		self.connection = None # reference to connected port
		self.type = DUAL
	def get_r(self):
		return Vector3(*self.parent.r,0)+self.r*self.parent.size()
	def is_free(self):
		return self.connection == None
	def is_compatible(self,p):
		return (self.type == DUAL) or (p.type == DUAL)
	def connect(self,p):
		p.connection = self
		self.connection = p
	def disconnect(self):
		if self.connection:
			self.connection.connection = None
			self.connection = None
	def get_connected_object(self):
		if self.connection:
			return self.connection.parent
		return None

class PoweredObject(PlacedObject):
	PORT_NUM = 1
	RANGE = 1
	CAPACITY = 1
	def __init__(self):
		super().__init__()
		self.PORTS = [Port(self,K3) for i in range(type(self).PORT_NUM)]
		self.production_rate = 0
		self.consumption_rate = 0
		self.stored = 0
		self.network = Network()
		self.network.objects.append(self)

	def is_full(self):
		return type(self).CAPACITY == self.stored
	
	def is_empty(self):
		return 0 == self.stored

	def flow(self, energy):
		self.stored += energy
		self.stored = min(self.stored,type(self).CAPACITY)
		self.stored = max(self.stored,0)
	
	def get_connected_objects(self):
		return [p.connection.parent for p in self.get_connected_ports()]

	def get_network_objects(self):
		def unite(l,l_): # returns l union l_
			for u in l_:
				if u not in l:
					l.append(u)
		explored_nodes = []
		nodes = [self]
		while len(nodes)!=0: # BFS
			n = nodes[0] # pop top
			nodes = nodes[1:]
			unite(explored_nodes,[n]) # mark as explored
			unite(nodes,[nb for nb in n.get_connected_objects() if nb not in explored_nodes])
		return explored_nodes


	def get_connected_ports(self):
		cp = []
		for p in self.PORTS:
			if not p.is_free():
				cp.append(p)
		return cp

	def get_free_ports(self):
		fp = []
		for p in self.PORTS:
			if p.is_free():
				fp.append(p)
		return fp

	def range_check(self,o):
		return (self.r - o.r).length() < max(type(self).RANGE,type(o).RANGE)

	def is_connectable(self,o):
		if o in self.get_connected_objects():
			return False
		if not self.range_check(o):
			return False
		for pu in o.get_free_ports():
			for pv in self.get_free_ports():
				if pu.is_compatible(pv):
					return True
		return False

	def connect(self,o):
		if not self.is_connectable(o):
			return False
		fp_s = self.get_free_ports()
		fp_o = o.get_free_ports()
		def key(pp):
			p1, p2 = pp
			return (p1.get_r()-p2.get_r()).length()
		# sort pairs of free ports by distance, extract closest pair
		list_pair_ports = [(pu,pv) for pu in fp_s for pv in fp_o if pu.is_compatible(pv)]
		list_pair_ports.sort(key=key)
		po, ps = list_pair_ports[0]
		po.connect(ps)
		return True
	
	def disconnect(self,o):
		if o not in self.get_connected_objects():
			return False
		if self not in o.get_connected_objects():
			return False
		for pu in o.PORTS:
			for pv in self.PORTS:
				if pu.get_connected_object() == self and pv.get_connected_object() == o:
					pu.disconnect()
					return True

class SingleSourcePoweredObject(PoweredObject):
	PORT_NUM = 1
	def __init__(self):
		super().__init__()
		for p in self.PORTS:
			p.type = OUTPUT

class SingleSinkPoweredObject(PoweredObject):
	PORT_NUM = 1
	def __init__(self):
		super().__init__()
		for p in self.PORTS:
			p.type = INPUT

		


		
		

