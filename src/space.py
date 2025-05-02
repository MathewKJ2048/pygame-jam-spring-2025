from conf import *
from object import *

class Space(GameObject):
	def __init__(self,parent=None):
		super().__init__(parent=parent)
		self.children = []

	def get_placed_objects(self):
		return [o for o in self.children if isinstance(o,PlacedObject)]

	def get_lines(self):
		return make_pair_list([
			(I3+J3)/2,
			(I3-J3)/2,
			(-I3-J3)/2,
			(-I3+J3)/2
		])

	def get_animated_lines(self):
		l = self.get_lines()
		f = min(self.time,1)
		if f == 1:
			return l
		return [(f*u,f*v) for u,v in l]

	def is_divided(self):
		for c in self.children:
			if type(c) == Space:
				return True
		return False

	def get_descendants(self):
		d = self.children
		for c in self.children:
			if type(c) == type(self):
				d+=c.get_descendants()
		return d

	def get_color(self):
		if self.level%2 == 0:
			return MAGENTA
		return CYAN
	
	def contains(self,o):
		diff_x = abs(self.r.x - o.r.x)
		diff_y = abs(self.r.y - o.r.y)
		return diff_x < self.size()/2 and diff_y < self.size()/2

	def subdivide(self):
		new_size = self.size()/SUBDIVISION
		for i in range(SUBDIVISION):
			for j in range(SUBDIVISION):
				s = Space(parent=self)
				s.r = self.r - (I+J)*self.size()/2 + (I+J)*new_size/2 + i*I*new_size + j*J*new_size
				self.children.append(s)

	def is_free(self):
		return len(self.get_placed_objects()) == 0
