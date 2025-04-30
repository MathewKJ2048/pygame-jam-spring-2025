from conf import *

def project(r,game):
	x = r.x
	y = r.y
	return (WIDTH/2+game.scale*x*CAMERA_CONSTANT_SCALE,HEIGHT/2-game.scale*y*CAMERA_CONSTANT_SCALE)

def project3(r,game):
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
		pygame.draw.aaline(surface,o.get_color(),pp[0],pp[1],width=o.get_width())

def render_space_base(surface,s,game):
	points = [project3(Vector3(s.r.x,s.r.y,0)+t[0]*s.size(),game) for t in s.get_lines()]
	pygame.draw.polygon(surface,darken(s.get_color(),0.5),points)


def render_builder(surface,b,game):
	render_object(surface, game.builder, game)

def render_selection_plate(surface,b,game):
	if not b.parent:
		return
	s = b.parent
	points = [project3(Vector3(s.r.x,s.r.y,0)+t[0]*s.size()*3/4,game) for t in s.get_lines()]
	pygame.draw.polygon(surface,WHITE,points,width=2)



def render(game):
	surface = pygame.Surface((WIDTH,HEIGHT))
	surface.fill(BACKGROUND)
	def key(s):
		return s.level
	game.spaces.sort(key=key)
	for s in game.spaces:
		render_space_base(surface,s,game)
	
	for s in game.spaces:
		render_object(surface,s,game)
	render_selection_plate(surface,game.builder,game)
	render_builder(surface, game.builder, game)
	return surface
