from conf import *
from object import *

class Bug(PlacedObject):
	def __init__(self):
		super().__init__()
		self.v = I
		self.time = 0
		self.target = None
		self.leg_positions_relative = [unit_vector3(i*math.pi/3) for i in range(6)]
	def evolve(self,dt):
		self.chase_target()
		self.r = self.r+self.v*dt*self.size()
		self.time+=dt
		self.legs_slide_back(dt)
		self.steps()
	def legs_slide_back(self,dt):
		change = Vector3(*self.v*dt,0)
		self.leg_positions_relative = [r - change for r in self.leg_positions_relative]
	def steps(self):
		ideal_relative_leg_positions = [unit_vector3(i*math.pi/3) for i in range(6)]
		for i in range(6):
			diff = ideal_relative_leg_positions[i]-self.leg_positions_relative[i]
			if diff.length()>GAIT:
				self.leg_positions_relative[i] = ideal_relative_leg_positions[i]

	def chase_target(self):
		if not self.target:
			return
		diff_r = self.target.r - self.r
		if diff_r.length()==0:
			return
		self.v = self.v.length()*diff_r.normalize()
	def get_lines(self):
		base = [K3/2+unit_vector3(i*math.pi/3)/4 for i in range(6)]
		top = [3*K3/4+unit_vector3(i*math.pi/3 + math.pi/6)/4 for i in range(6)]
		forward_connections = [(base[i],top[i]) for i in range(6)]
		backward_connections = [(top[i],base[(i+1)%6]) for i in range(6)]
		legs = [(base[i],self.leg_positions_relative[i]) for i in range(6)]
		return make_pair_list(base)+make_pair_list(top)+forward_connections+backward_connections+legs
		
