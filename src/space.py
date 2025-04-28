from conf import *
from object import *

class Space(Object):
	def __init__(parent=None):
		super.__init__()
		if parent:
			self.parent = parent
			self.level = parent.level+1
			self.size = self.parent.size/SUBDIVISION
		else:
			self.level = 0
			self.size = 1
	def contains(r):
		diff_x = abs(self.x - r.x)
		diff_y = abs(self.y - r.y)
		return diff_x < self.size/2 and diff_y < self.size/2

	def subdivide():
		pass
