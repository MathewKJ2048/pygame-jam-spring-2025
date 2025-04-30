from conf import *

def clip(x,m): # between 0 and m
	x = max(x,0)
	x = min(x,m)
	return x

def clip_point_pair(pp):
	x1, y1 = pp[0]
	x2, y2 = pp[1]
	def get_p(t): # x1(t)+x2(1-t) = xt
		return (t*x1+(1-t)*x2,t*y1+(1-t)*y2)
	def get_t(u1,u2,u): # (u - u2)/(u1-u2)
		if u1 == u2:
			return None
		return (u-u2)/(u1-u2)
	def inside(t):
		X, Y = get_p(t)
		return X >= XMIN and X <= XMAX and Y <= YMAX and Y >= YMIN
	t1 = get_t(x1,x2,XMIN)
	t2 = get_t(x1,x2,XMAX)
	t3 = get_t(y1,y2,YMIN)
	t4 = get_t(y1,y2,YMAX)
	ts = []
	for t in [0,1,t1,t2,t3,t4]:
		if t == None:
			continue
		if not inside(t):
			continue
		if 0 <= t and t <= 1:
			ts.append(t)
	if len(ts)<2:
		return None
	return (get_p(min(ts)),get_p(max(ts)))

def draw_line(surface,pp,color,width):
	pp = clip_point_pair(pp)
	if pp:
		pygame.draw.aaline(surface,color,pp[0],pp[1],width=width)
	


	



def project(r,game):
	x = r.x
	y = r.y
	X = WIDTH/2+game.scale()*x*CAMERA_CONSTANT_SCALE
	Y = HEIGHT/2-game.scale()*y*CAMERA_CONSTANT_SCALE
	return (X,Y)

def project3(r_,game):
	r = r_ - Vector3(*game.camera,0)
	theta = game.camera_angle
	phi = theta+2*math.pi/3
	I_transform = unit_vector(theta)
	J_transform = unit_vector(phi)
	K_transform = unit_vector(math.pi/2)
	v = r.x*I_transform + r.y*J_transform + r.z*K_transform
	return project(v,game)


def render_object(surface,o,game):
	r0 = Vector3(o.r.x,o.r.y,0)
	pairs = o.get_lines()
	def transform(r):
		return project3(r0 + r*o.size(),game)
	def transform_pair(p):
		u, v = p
		return (transform(u),transform(v))
	point_pairs = [transform_pair(l) for l in pairs]
	for pp in point_pairs:
		draw_line(surface,pp,o.get_color(),o.get_width())
		

def render_space_base(surface,s,game):
	points = [project3(Vector3(s.r.x,s.r.y,0)+t[0]*s.size(),game) for t in s.get_lines()]
	pygame.draw.polygon(surface,darken(s.get_color(),0.5),points)


def render_builder(surface,b,game):
	temp = game.builder.level
	game.builder.level = game.camera_level+1
	render_object(surface, game.builder, game)
	game.builder.level = temp

def render_selection_plate(surface,b,game):
	if not b.parent:
		return
	s = b.parent
	points = [project3(Vector3(s.r.x,s.r.y,0)+t[0]*s.size()*3/4,game) for t in s.get_lines()]
	pygame.draw.polygon(surface,WHITE,points,width=2)





def render(game):
	surface = pygame.Surface((WIDTH,HEIGHT))
	surface.fill(BACKGROUND)

	def filter_list_objects(lobj):
		filtered = []
		for o in lobj:
			if o.level <= game.camera_level+3:
				filtered.append(o)
		return filtered

	spaces = filter_list_objects(game.spaces)
	objects = filter_list_objects(game.objects)

	def key(s):
		return s.level
	spaces.sort(key=key)
	for s in spaces:
		#render_space_base(surface,s,game)
		pass
	
	for s in spaces:
		render_object(surface,s,game)
	for o in objects:
		render_object(surface, o, game)
	render_selection_plate(surface,game.builder,game)
	render_builder(surface, game.builder, game)
	return surface
