from conf import *

class GameObject:
	def __init__(self,parent=None):
		self.r = Vector2(0,0)
		self.set_parent(parent)
	def size(self):
		return SUBDIVISION**(-self.level)
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

class PlacedObject(GameObject):
	def set_parent(self,parent):
		if parent:
			self.parent = parent
			self.level = parent.level
		else:
			self.parent = None
			self.level = 0

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
		self.connection.connection = None
		self.connection = None
	def get_connected_object(self):
		return self.connection.parent

class PoweredObject(PlacedObject):
	PORT_NUM = 1
	RANGE = 1
	CAPACITY = 0
	def __init__(self):
		super().__init__()
		self.PORTS = [Port(self,Vector3(0,0,0)) for i in range(type(self).PORT_NUM)]
		self.production_rate = 0
		self.consumption_rate = 0
		self.stored = 0
	
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
		for pu in o.ports:
			for pv in self.ports:
				if pu.get_connected_object() == self and pv.get_connected_object() == o:
					pu.disconnect(pv)
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

		


		
		

