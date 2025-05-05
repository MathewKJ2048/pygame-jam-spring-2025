from conf import *

class Particle:
	def __init__(self,r,shift=0):
		self.level = 0
		self.time = 0
		self.max_time = 1
		self.r = Vector3(0,0,0)
		self.r.x = r.x
		self.r.y = r.y
		if type(r)==Vector3:
			self.r.z = r.z
		else:
			self.r.z = shift
		self.v = K3
		self.color = (20,20,20)
		self.radius = 1

	def evolve(self,dt):
		self.time+=dt
		self.r+=self.v*dt*(SUBDIVISION**self.level)
	def get_radius(self):
		f = min(1,self.time/self.max_time)
		return (1-f)*self.radius

def explosion(number,r,max_v,min_v,bias_v,radius,color):
	sqrt3 = math.sqrt(3)
	particles = []
	def rand_v():
		return (max_v+random.random()*(max_v-min_v))
	for i in range(number):
		p = Particle(r,shift = 1/2)
		p.color = color
		p.radius = radius
		th = random.random()*2*math.pi
		ph = random.random()*math.pi/2
		v = rand_v()
		p.v = v*Vector3(math.cos(th)*math.sin(ph),math.sin(th)*math.sin(ph),math.cos(ph))/sqrt3 + bias_v
		particles.append(p)
	return particles
		
		



	
