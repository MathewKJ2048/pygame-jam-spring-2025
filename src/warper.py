from conf import *
from object import *

class Warper(SingleSinkPoweredObject):
	def get_color(self):
		if self.level%2 == 0:
			return CYAN
		return MAGENTA
	def get_lines(self):
		n = 4
		height = 1
		base = [unit_vector3(i*math.pi*2/n + math.pi/4) for i in range(n)]
		bottom = [b/math.sqrt(2) for b in base]
		top = K3
		return make_pair_list(bottom)+join(bottom,top)