from conf import *
from object import *

class Builder(GameObject):
	def __init__(self):
		super().__init__()
		self.v = Vector2(0,0)
		self.scale = 1
	def evolve(self,dt):
		self.r+=self.v*dt


