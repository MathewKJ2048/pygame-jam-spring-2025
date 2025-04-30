from conf import *
from object import *

class Engine(PoweredObject):
	PORT_NUM = 1
	energy_rate = 1
	def __init__(self):
		super().__init__()
		for p in self.PORTS:
			p.type = OUTPUT
	def get_energy(dt):
		return Engine.energy_rate*dt
	def get_color(self):
		return YELLOW