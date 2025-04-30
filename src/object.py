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
	def size(self):
		return SUBDIVISION**(-self.level+1)

class Port:
	def __init__(self,parent,r):
		self.parent = parent
		self.r = r # position of port relative to parent
		self.connection = None # reference to connected port
	def get_r():
		return self.parent.r+self.r*self.parent.size()
	def is_free(self):
		return self.connection == None
	def connect(self,p):
		p.connection = self
		self.connection = p
	def disconnect(self):
		self.connection.connection = None
		self.connection = None
	def get_connected_object(self):
		return self.connection.parent

class PoweredObject(PlacedObject):
	PORT_NUM = 4
	RANGE = 1
	def __init__(self):
		super().__init__()
		self.PORTS = [Port(Vector3(0,0,0)) for i in range(type(self).PORT_NUM)]
	
	def get_connected_objects(self):
		return [p.connection.parent for p in self.PORTS]

	def get_free_ports(self):
		fp = []
		for p in self.ports:
			if p.is_free():
				fp.append(c)
		return fp

	def connect(self,o):
		if o in self.get_connected_objects():
			return False
		fp_s = self.get_free_ports()
		fp_o = o.get_free_ports()
		if len(fp_o)==0 or len(fp_s)==0:
			return False
		def key(pp):
			p1, p2 = pp
			return (p1.get_r()-p2.get_r()).length()
		# sort pairs of free ports by distance, extract closest pair
		po, ps = [(pu,pv) for pu in fp_s for pv in fp_o].sort(key=key)[0]
		if (po.get_r()-ps.get_r()).length() > max(type(self).RANGE,type(o).RANGE):
			return False
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

		


		
		

