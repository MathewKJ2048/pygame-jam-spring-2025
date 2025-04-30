from conf import *
from object import *

class Tower(PoweredObject):
	PORT_NUM = 6
	RANGE = 4
	def __init__(self):
		super().__init__()
		n = Tower.PORT_NUM
		base = [unit_vector3(i*2*math.pi/n) for i in range(n)]
		tower_arm_tips = [b/4+3*K3/4 for b in base]
		self.PORTS = [Port(self,t) for t in tower_arm_tips]
	def get_lines(self):
		tower_base = K3/8
		tower_top = K3/2

		n = Tower.PORT_NUM
		base = [unit_vector3(i*2*math.pi/n) for i in range(n)]
		pedestal_low = [b/4 for b in base]
		pedestal_high = [b/4+tower_base for b in base]
		pedestal = [(pedestal_high[i],pedestal_low[i]) for i in range(n)]+make_pair_list(pedestal_high)+make_pair_list(pedestal_low)+[(pedestal_high[i],tower_base) for i in range(n)]

		tower_arm_tips = [b/4+3*K3/4 for b in base]
		tower = [(tower_base,tower_top)]+[(tower_top,t) for t in tower_arm_tips]
		return pedestal+tower
		pass

class HighTower(PoweredObject):
	PORT_NUM = 3
	RANGE = 8
	def __init__(self):
		super().__init__()
		n = 2*HighTower.PORT_NUM
		tower_tips = [K3+unit_vector3(i*2*math.pi/(n/2))/2 for i in range(n//2)]
		self.PORTS = [Port(self,t) for t in tower_tips]
	def get_lines(self):
		n = 2*HighTower.PORT_NUM
		base = [unit_vector3(i*2*math.pi/n) for i in range(n)]
		bottom = [b/2 for b in base]
		l0 = [b/4+K3/8 for b in base]
		l1 = [b/4+3*K3/8 for b in base]
		l2 = [b/4+5*K3/8 for b in base]
		l3 = [b/4+7*K3/8 for b in base]

		def triple_cross_hatch(l1,l2):
			M = len(l1)
			return [(l1[i],l2[i]) for i in range(M)]

		pedestal = make_pair_list(bottom)+make_pair_list(l0)+[(l0[i],bottom[i]) for i in range(n)]
		body = make_pair_list(l1)+triple_cross_hatch(l0,l1)+make_pair_list(l2)+triple_cross_hatch(l1,l2)+make_pair_list(l3)+triple_cross_hatch(l2,l3)
		tower_tips = [K3+unit_vector3(i*2*math.pi/(n/2))/2 for i in range(n//2)]
		petals = [(tower_tips[i],l2[2*i]) for i in range(n//2)]+[(tower_tips[i],l3[2*i+1]) for i in range(n//2)]+[(tower_tips[i],l3[(2*i-1+n)%n]) for i in range(n//2)]

		return pedestal+body+petals