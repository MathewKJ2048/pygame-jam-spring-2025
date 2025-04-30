from conf import *
from object import *

class Builder(PlacedObject):
	def __init__(self):
		super().__init__()
		self.v = Vector2(0,0)
		self.time = 0
	def evolve(self,dt):
		self.r+=self.v*self.size()*dt
		self.time+=dt
	def get_lines(self):
		n = 8
		BASE = [unit_vector3(t*math.pi*2/n+BUILDER_ANGULAR_VELOCITY*self.time) for t in range(n)]
		L1 = [b/2 + K3 for b in BASE]
		L2 = [b/4 + K3 + K3/4 for b in BASE]
		panel_lines = [(L1[i],L2[i]) for i in range(len(L1))]
		return make_pair_list(L1)+make_pair_list(L2)+panel_lines

