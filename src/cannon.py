from conf import *
from object import *
from bug import *

class Cannon(PoweredObject):
	RANGE = 5
	FIRING_TIME = 4
	DAMAGE_RATE = 1/2
	MAX_WIDTH = 1/4
	opening_time_fraction = 0.2
	def __init__(self):
		super().__init__()
		self.aim_vector = I
		self.target = None
		self.last_fired_time = -100
		self.PORTS = [Port(self,K3-K3)]

	def evolve(self,dt):
		super().evolve(dt)
		self.fire()
		self.burn_target(dt)
	
	def set_target(self,objects):
		self.target = None
		bugs = [b for b in objects if type(b) == Bug and (b.r-self.r).length()<type(self).RANGE and b.level == self.level]
		if len(bugs) == 0:
			return
		bugs.sort(key=lambda o: -self.aim_vector.dot(set_max(o.r-self.r,1)))
		self.target = bugs[0]
		self.aim_vector = (self.target.r-self.r).normalize()
		
		
	def get_color(self):
		return PURPLE

	def burn_target(self,dt):
		# ablates target health if currently firing
		if not self.target:
			self.consumption_rate = 0
			return
		diff_time = self.time - self.last_fired_time
		if not diff_time < type(self).FIRING_TIME:
			self.consumption_rate = 0
			return
		th = type(self).opening_time_fraction*type(self).FIRING_TIME
		if diff_time <= th and diff_time+dt>th:
			play_sound(laser_sound)
		self.consumption_rate = 8
		damage = type(self).DAMAGE_RATE*dt
		self.target.cause_damage(damage)

	def fire(self): # resets the fire time if not currently firing, and nothing else
		if not self.target:
			return False
		if self.time - self.last_fired_time < type(self).FIRING_TIME:
			return False
		if self.stored != type(self).CAPACITY:
			return False
		self.last_fired_time = self.time
		return True

	def get_particles(self):
		k = self.get_k()
		if self.target and k==1:
			return explosion(10,self.target.r,5,2,K3-K3,0.2,darken(GREEN,0.1))
		return []


	def get_firing_lines(self):
		f = self.get_f()
		k = self.get_k()
		if f == 1:
			return []

		answer = []

		if k == 1 and self.target:
			d = (self.target.r-self.r)/self.size()
			answer.append((K3/2,Vector3(d.x,d.y,1/2)))

		av, p1, p2 = self.get_av_p1_p2()
		NP = 6
		NL = 4
		w = type(self).MAX_WIDTH*k
		def get_perp_unit(theta):
			return K3*math.cos(theta)+p1*math.sin(theta)
		
		def get_polygon(power_base,i):
			return [p*w + av*(i/NL - 1/2)/2 + K3/2 for p in power_base]

		def get_angles(f):
			return [math.pi*2*i/NP + math.pi*2*f for i in range(NP)]

		def get_power_base(f):
		    return [get_perp_unit(theta) for theta in get_angles(f)]

		polygons = [get_polygon(get_power_base(f*(-1)**i),i) for i in range(NL)]
		for i in range(NL):
			answer+=make_pair_list(polygons[i])
		
		return answer

	def get_av_p1_p2(self):
		av = Vector3(*self.aim_vector,0)
		p1 = Vector3(-av.y,av.x,0)
		p2 = Vector3(av.y,-av.x,0)
		return av, p1, p2
	
	def get_f(self): # 0 at start of firing to 1 at end, 1 if not firing
		return min((self.time-self.last_fired_time)/type(self).FIRING_TIME,1)
	
	def get_k(self): # ranges from 0 to 1 with a plateau at t
		f = self.get_f()
		return min(f,1-f,type(self).opening_time_fraction)/type(self).opening_time_fraction

	def get_lines(self):
		
		n = 6
		m = 2*n
		w = type(self).MAX_WIDTH

		k = self.get_k() 
		wc = w * math.sin(k*math.pi/2)
		av, p1, p2 = self.get_av_p1_p2()
		base = [unit_vector3(math.pi*2*i/n) for i in range(n)]
		bottom = [b/2 for b in base]
		top = [b*w+K3/8 for b in base]
		mount = [K3/8+unit_vector3(math.pi*2*i/m)*w for i in range(m)]
		pedestal = make_pair_list(mount)+make_pair_list(bottom)+interweave(top,bottom)
		cannon_base = [K3/8,K3/2+av,7*K3/8,K3/2-av/2]
		left_base = [c+(wc*p1) for c in cannon_base]
		right_base = [c+(wc*p2) for c in cannon_base]
		cannon = join(left_base,(w+wc)*p1+K3/2)+join(right_base,(w+wc)*p2+K3/2)+make_pair_list(left_base)+make_pair_list(right_base)
		
		
		return pedestal+cannon