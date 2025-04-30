from conf import *
from object import *

class Tower(PlacedObject):
	MAX_CONNECTIONS = 8
	RANGE = 2
	def get_lines(self):
		tower_base = K3/8
		tower_top = K3/2

		n = Tower.MAX_CONNECTIONS
		base = [unit_vector3(i*2*math.pi/n) for i in range(n)]
		pedestal_low = [b/4 for b in base]
		pedestal_high = [b/4+tower_base for b in base]
		pedestal = [(pedestal_high[i],pedestal_low[i]) for i in range(n)]+make_pair_list(pedestal_high)+make_pair_list(pedestal_low)+[(pedestal_high[i],tower_base) for i in range(n)]

		tower_arm_tips = [b/4+3*K3/4 for b in base]
		tower = [(tower_base,tower_top)]+[(tower_top,t) for t in tower_arm_tips]
		return pedestal+tower
		pass

class HighTower(PlacedObject):
	MAX_CONNECTIONS = 3
	RANGE = 8
	pass