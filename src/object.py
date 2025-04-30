from conf import *

class GameObject:
	color = WHITE
	def __init__(self,parent=None):
		self.r = Vector2(0,0)
		self.set_parent(parent)
	def size(self):
		return SUBDIVISION**(-self.level)
	def set_parent(self,parent):
		if parent:
			self.parent = parent
			self.level = parent.level+1
		else:
			self.parent = None
			self.level = 0
