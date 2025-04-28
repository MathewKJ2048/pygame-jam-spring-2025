from conf import *

class GameObject:
	def __init__(self):
		self.r = Vector2(0,0)
		self.parent = None
		self.children = []