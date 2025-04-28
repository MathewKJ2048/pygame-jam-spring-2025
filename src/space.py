from conf import *
from object import *

class Space(GameObject):
	def __init__(self,parent=None):
		super().__init__()
		if parent:
			self.parent = parent
			self.level = parent.level+1
			self.size = self.parent.size/SUBDIVISION
		else:
			self.level = 0
			self.size = 1
	def contains(self,o):
		diff_x = abs(self.r.x - o.r.x)
		diff_y = abs(self.r.y - o.r.y)
		return diff_x < self.size/2 and diff_y < self.size/2

	def subdivide():
		pass
