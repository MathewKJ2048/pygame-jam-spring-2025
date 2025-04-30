from conf import *
from object import *

class Engine(PlacedObject):
	energy_rate = 1
	def get_energy(dt):
		return Engine.energy_rate*dt
	def get_color(self):
		return YELLOW