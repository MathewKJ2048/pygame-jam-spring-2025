from conf import *
from object import *

class Engine(SingleSourcePoweredObject):
	def __init__(self):
		super().__init__()
		self.production_rate=1
	def get_color(self):
		return WHITE