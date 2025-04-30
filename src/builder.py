from conf import *
from object import *

class Builder(PlacedObject):
	def __init__(self):
		super().__init__()
		self.v = Vector2(0,0)
	def evolve(self,dt):
		self.r+=self.v*self.size()*dt

