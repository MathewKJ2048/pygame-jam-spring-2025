from conf import *

class Object:
	def __init__(self):
		self.r = Vector2(0,0)
		self.parent = None
		self.children = []