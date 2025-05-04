from conf import *
from object import *
from engine import *





class Bug(PlacedObject):
	UID = 0
	def __init__(self):
		super().__init__()
		self.UID = Bug.UID
		Bug.UID+=1
		self.v = I
		self.speed = 1
		self.time = 0
		self.target = None
		self.color = (200,100,0)
		self.compute_geometry()
		
	
	def compute_geometry(self):
		self.N = 4
		self.IDEAL_LEG_POSITIONS_RELATIVE = [unit_vector3(i*2*math.pi/self.N) for i in range(self.N)]
		self.BASE = [K3/2+t/4 for t in self.IDEAL_LEG_POSITIONS_RELATIVE]
		offset = [
			((self.IDEAL_LEG_POSITIONS_RELATIVE[i]+self.IDEAL_LEG_POSITIONS_RELATIVE[(i+1)%self.N])/2)
			.normalize()*self.IDEAL_LEG_POSITIONS_RELATIVE[i].length() for i in range(self.N)]
		self.TOP = [3*K3/4+t/4 for t in offset]
		self.L1 = (self.BASE[0]-self.IDEAL_LEG_POSITIONS_RELATIVE[0]).length()
		self.L2 = self.L1

		self.leg_positions_relative = self.IDEAL_LEG_POSITIONS_RELATIVE.copy()
		self.target_leg_positions = self.IDEAL_LEG_POSITIONS_RELATIVE.copy()
		
	def evolve(self,dt):
		super().evolve(dt)
		self.r = self.r+self.v*dt*self.size()
		self.legs_slide_back(dt)
		self.update_target_leg_positions()
		self.steps(dt)
	def get_color(self):
		return self.color
	def get_width(self):
		return 4
	def legs_slide_back(self,dt):
		change = Vector3(*self.v*dt,0)
		self.leg_positions_relative = [r - change for r in self.leg_positions_relative]
		self.target_leg_positions = [r - change for r in self.target_leg_positions]

	def set_target(self,object_list,backup_target=None):
		target_object_list = [o for o in object_list if type(o) == Engine]
		if len(target_object_list) == 0:
			self.target = backup_target
		else:
			target_object_list.sort(key=lambda o: (self.r-o.r).length())
			self.target = target_object_list[0]

		THRESHHOLD = 1
		bugs_swarm = [b for b in object_list if type(b)==Bug and (b.r-self.r).length()<=1 and b!=self]
		direction = self.target.r - self.r
		submissive = any([b.UID > self.UID for b in bugs_swarm]) # in presence of later bugs
		diff_r = Vector2(0,0)
		if not submissive:
			diff_r = set_max(direction,1) # dominant bug chases targets, submissive bugs maintain swarm
		for b in bugs_swarm:
			if b.UID > self.UID: # all bugs repelled by bugs later than them
				diff_r+=(self.r-b.r).normalize()
		self.v = self.speed*set_max(diff_r,1)
		return


		if diff_r.length()>THRESHHOLD:
			diff_r = set_max(diff_r,1)
			submissive = False
			for b in bugs_swarm:
				if self.UID<b.UID:
					submissive = True
				diff_r+=(self.r-b.r).normalize()
			if submissive:
				self.diff_r -= 0
		self.v = self.speed*set_max(diff_r,1)



	def get_moving_feet(self):
		needs_moving = []
		for i in range(self.N):
			if (self.leg_positions_relative[i]-self.target_leg_positions[i]).length()>0.001:
				needs_moving.append(i)

		# two adjacent legs can't move, opposite leg cannot move
		movement = []
		for i in needs_moving:
			nb1 = (i-1+self.N)%self.N
			nb2 = (i+1)%self.N
			opp = (i+self.N//2)%self.N
			L = (self.BASE[i] - self.leg_positions_relative[i]).length()
			alright = 1.1*L<self.L1+self.L2
			if (nb1 not in movement and nb2 not in movement and opp not in movement) or not alright:
				movement.append(i)
		return movement

	def steps(self,dt):
		movement = self.get_moving_feet()
		for i in range(self.N):
			if i not in movement:
				continue
			self.leg_positions_relative[i] = lerp_approach(
				self.leg_positions_relative[i],
				self.target_leg_positions[i],5*self.v.length(),dt)

	def update_target_leg_positions(self):
		for i in range(self.N):
			drift = abs(self.IDEAL_LEG_POSITIONS_RELATIVE[i].length()-self.leg_positions_relative[i].length())
			diff = (self.IDEAL_LEG_POSITIONS_RELATIVE[i] - self.leg_positions_relative[i]).length()
			if drift>GAIT or diff>0.5:
				self.target_leg_positions[i] = self.IDEAL_LEG_POSITIONS_RELATIVE[i]




	def get_lines(self):
		ankles = [t for t in self.leg_positions_relative]

		forward_connections = interweave(self.BASE,self.TOP,offset=-1)
		backward_connections = interweave(self.BASE,self.TOP,offset=1)
		lower = join(self.BASE,K3/4)
		upper = join(self.TOP,K3/4)

		knees = [solve(self.L1,self.L2,ankles[i],self.BASE[i]) for i in range(self.N)]
		thighs = interweave(self.BASE,knees)
		calves = interweave(knees, ankles)
		feet = []
		for i in range(self.N):
			t = ankles[i]
			feet+=[(t,t+unit_vector3(i*2*math.pi/3)/6) for i in range(3)]
	
		return make_pair_list(self.BASE)+make_pair_list(self.TOP)+forward_connections+backward_connections+upper+lower+thighs+calves+feet
		
