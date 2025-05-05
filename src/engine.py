from conf import *
from object import *

class Engine(SingleSourcePoweredObject):
	CAPACITY = 0
	def __init__(self):
		super().__init__()
		self.production_rate=1
	def get_color(self):
		return RED
	def get_width(self):
		return 2
	def get_lines(self):
		n = 4
		m = 4
		bases = [[unit_vector3(math.pi*2*i/n + self.time*(-1)**j)/4+K3*j/(m*2) for i in range(n)] for j in range(m)]
		answer = [(K3-K3,K3)]
		for b in bases:
			answer+=make_pair_list(b)
		return answer