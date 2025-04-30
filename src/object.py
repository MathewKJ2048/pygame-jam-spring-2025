from conf import *

class GameObject:
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
	def get_lines(self):
		return [(I3/2,-I3/2),(J3/2,-J3/2),(I3-I3,K3)]
	def get_color(self):
		return WHITE
	def get_width(self):
		return 2

class PlacedObject(GameObject):
	def size(self):
		return SUBDIVISION**(-self.level+1)
