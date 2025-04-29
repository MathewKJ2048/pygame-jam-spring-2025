from conf import *

class GameObject:
	def __init__(self,parent=None):
		self.r = Vector2(0,0)
		if parent:
			self.parent = parent
			self.level = parent.level+1
		else:
			self.parent = None
			self.level = 0