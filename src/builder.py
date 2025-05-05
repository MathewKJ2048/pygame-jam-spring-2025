from conf import *
from object import *

class Builder(MovingObject):
	def __init__(self):
		super().__init__()
		self.v = Vector2(0,0)
	def get_lines(self):
		n = 8
		BASE = [unit_vector3(t*math.pi*2/n+BUILDER_ANGULAR_VELOCITY*self.time) for t in range(n)]
		L1 = [b/2 + K3 for b in BASE]
		L2 = [b/4 + K3 + K3/4 for b in BASE]
		return make_pair_list(L1)+make_pair_list(L2)+interweave(L1,L2)
	def get_particles(self):
		return explosion(self.get_render_size(),1,Vector3(*self.r,1),1,0,-2*K3,0.1,darken(YELLOW,0.1))

