from conf import *
from game import *

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
		pygame.draw.line(surface,color,pp[0],pp[1],width=width)
	

def project(r,game):
	x = r.x
	y = r.y
	X = WIDTH/2+game.scale()*x*CAMERA_CONSTANT_SCALE
	Y = HEIGHT/2-game.scale()*y*CAMERA_CONSTANT_SCALE
	return (X,Y)

def project3(r_,game):
	r = r_ - Vector3(*game.camera,0)
	r = rotate_xy(r,game.camera_angle)
	v = r.x*I_transform + r.y*J_transform + r.z*K_transform
	return project(v,game)

def render_pair_list(surface,r0,size,game,color, width, pairs):
	def transform(r):
		return project3(r0 + r*size,game)
	def transform_pair(p):
		u, v = p
		return (transform(u),transform(v))
	point_pairs = [transform_pair(l) for l in pairs]
	for pp in point_pairs:
		draw_line(surface,pp,color,width)

def render_object(surface,o,game):
	r0 = Vector3(o.r.x,o.r.y,0)
	render_pair_list(surface,r0,o.get_render_size(),game,o.get_color(),o.get_width(),o.get_animated_lines())
	if isinstance(o,PoweredObject):
		if type(o).CAPACITY!=0:
			f = o.stored/type(o).CAPACITY
			render_pair_list(surface,r0,o.get_render_size(),game,YELLOW,2,
			make_pair_list([f*t/2 for t in [I3+J3,I3-J3,-J3-I3,J3-I3]]))
	
		

def render_space_base(surface,s,game):
	points = [project3(Vector3(s.r.x,s.r.y,0)+t[0]*s.size(),game) for t in s.get_lines()]
	pygame.draw.polygon(surface,darken(s.get_color(),0.5),points)


def render_builder(surface,b,game):
	# temp = game.builder.level
	# game.builder.level = game.camera_level
	render_object(surface, game.builder, game)
	# game.builder.level = temp

def render_ray(surface,c,game):
	render_pair_list(surface,Vector3(*c.r,0),c.size(),game,GREEN,5,c.get_firing_lines())

def render_particle(surface,p,game):
	if abs(p.level - game.camera_level)>2:
		return
	R = p.get_radius()*(SUBDIVISION**game.camera_level)*CAMERA_CONSTANT_SCALE
	particle_surface = pygame.Surface((2*R,2*R))
	particle_surface.fill(BACKGROUND)
	pygame.draw.circle(particle_surface,p.color,(R,R),R)
	X, Y = project3(p.r,game)
	surface.blit(particle_surface,(X-R,Y-R),special_flags=pygame.BLEND_RGB_ADD)
	# pygame.draw.circle(surface,p.color,project3(p.r,game),p.radius*(SUBDIVISION**p.level)*CAMERA_CONSTANT_SCALE)


def render_selection_plate(surface,b,game):
	if not b.parent:
		return
	s = b.parent
	points = [project3(Vector3(s.r.x,s.r.y,0)+t[0]*s.size()*3/4,game) for t in s.get_lines()]
	pygame.draw.polygon(surface,WHITE,points,width=2)

def render_wires(surface,object_list,game):
	for o in object_list:
		if not isinstance(o,PoweredObject):
			continue
		for p in o.PORTS:
			if p.is_free():
				continue
			pp = (project3(p.get_r(),game),project3(p.connection.get_r(),game))
			draw_line(surface,pp,YELLOW,5)

def get_minimap(game):
	def mini_project(r):
		t = r - game.camera
		S = MINI_SCALE*(SUBDIVISION**game.camera_level)
		return (MINI_WIDTH/2+t.x*S, MINI_HEIGHT/2-t.y*S)
	surface = pygame.Surface((MINI_WIDTH,MINI_HEIGHT))
	surface.fill(BACKGROUND)
	pygame.draw.circle(surface,game.builder.get_color(),mini_project(game.builder.r),2)
	mini_objects = [o for o in game.objects if o.level<=game.builder.level ]
	for o in mini_objects:
		if type(o) != Bug and type(o) not in [Tower, HighTower]:
			pygame.draw.circle(surface,o.get_color(),mini_project(o.r),BLIP_RADIUS)
	for o in mini_objects:
		if isinstance(o,PoweredObject):
			for t in o.get_connected_objects():
				pygame.draw.line(surface,YELLOW,mini_project(o.r),mini_project(t.r))
	for o in mini_objects:
		if type(o) == Bug:
			pygame.draw.circle(surface,(200,20,20),mini_project(o.r),BLIP_RADIUS)
	return surface

def render(game):
	surface = pygame.Surface((WIDTH,HEIGHT))
	surface.fill(BACKGROUND)

	for p in game.particles:
		render_particle(surface,p,game)

	def filter_list_objects(lobj):
		filtered = []
		for o in lobj:
			# distance more than max distance seen by camera + max distance covered by object
			if (o.r-game.camera).length() > 2*o.size() + 8*(SUBDIVISION**game.camera_level):
				continue
			if o.level <= game.camera_level+3:
				filtered.append(o)
		return filtered

	spaces = filter_list_objects(game.spaces)
	objects = filter_list_objects(game.objects)
	log("number rendered",len(spaces)+len(objects))

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
		if type(o) == Cannon:
			render_ray(surface, o, game)
	render_selection_plate(surface,game.builder,game)
	render_wires(surface,game.objects,game)
	render_builder(surface, game.builder, game)

	if game.minimap:
		surface.blit(get_minimap(game),(0,0))

	return surface
