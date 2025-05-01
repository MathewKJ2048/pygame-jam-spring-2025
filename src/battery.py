from conf import *
from object import *

class Battery(PoweredObject):
	def get_color(self):
		return GREEN
	def get_lines(self):
		n = 4
		height = 1
		base = [unit_vector3(i*math.pi*2/n + math.pi/4) for i in range(n)]
		bottom = [b/2 for b in base]
		top = [b/2+K3*height for b in base]
		return make_pair_list(top)+make_pair_list(bottom)+interweave(bottom,top)
