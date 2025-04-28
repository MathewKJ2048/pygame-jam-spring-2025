from conf import *
from object import *

class Builder:
	def __init__(self):
		self.r = Vector2(0,0)
		self.v = Vector2(0,0)
		self.scale = 1
	def evolve(self,dt):
		self.r+=self.v*dt


