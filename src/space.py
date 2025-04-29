from conf import *
from object import *

class Space(GameObject):
	def __init__(self,parent=None):
		super().__init__(parent=parent)
		self.children = []
	
	def contains(self,o):
		diff_x = abs(self.r.x - o.r.x)
		diff_y = abs(self.r.y - o.r.y)
		return diff_x < self.size()/2 and diff_y < self.size()/2

	def subdivide(self):
		if len(self.children) != 0:
			return False
		new_size = self.size()/SUBDIVISION
		for i in range(SUBDIVISION):
			for j in range(SUBDIVISION):
				s = Space(parent=self)
				s.r = self.r - (I+J)*self.size()/2 + (I+J)*new_size/2 + i*I*new_size + j*J*new_size
				self.children.append(s)
		return True
