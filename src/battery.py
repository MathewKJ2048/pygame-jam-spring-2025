from conf import *
from object import *

class Battery(PoweredObject):
	CAPACITY = 10
	def get_color(self):
		return GREEN
	def __init__(self):
		super().__init__()
		self.PORTS = [Port(self,K3/2)]
	def get_lines(self):
		n = 4
		height = 1
		base = [unit_vector3(i*math.pi*2/n + math.pi/4) for i in range(n)]
		bottom = [b/4 for b in base]
		top = [b/4+K3*height/2 for b in base]
		return make_pair_list(top)+make_pair_list(bottom)+interweave(bottom,top)
