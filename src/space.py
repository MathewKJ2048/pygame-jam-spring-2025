from conf import *
from object import *

class Space(GameObject):
	def __init__(self,parent=None):
		super().__init__()
		self.children = []
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

	def subdivide(self):
		if len(self.children) != 0:
			return False
		N = SUBDIVISION
		new_size = self.size/N
		ct = 0
		for i in range(N):
			for j in range(N):
				ct+=1
				s = Space(parent=self)
				s.r = self.r - (I+J)*self.size/2 + (I+J)*new_size/2 + i*I*new_size + j*J*new_size
				self.children.append(s)
		assert ct == SUBDIVISION*SUBDIVISION
		return True
