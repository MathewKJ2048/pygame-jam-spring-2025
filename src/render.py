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
	

def render_space(surface,s,game,color_override = None):
	r = Vector3(s.r.x,s.r.y,0)
	neighbours = [Vector3(1/2,1/2,0),Vector3(1/2,-1/2,0),Vector3(-1/2,-1/2,0),Vector3(-1/2,1/2,0)]
	screen_points = [project3(r+n*s.size(),game) for n in neighbours]
	color = MAGENTA
	if s.level % 2 == 1:
		color = CYAN
	if color_override:
		color = color_override
	pygame.draw.polygon(surface,color,screen_points,width=1)

def render_object(surface,o,game):
	r = Vector3(o.r.x,o.r.y,0)
	size = CAMERA_CONSTANT_SCALE/2 * game.scale * o.size()
	pygame.draw.aacircle(surface,(100,100,100),project3(r,game),size)

def render_builder(surface,b,game):
	render_object(surface, game.builder, game)
	if b.parent:
		render_space(surface, b.parent, game, color_override=WHITE)

def render(game):
	surface = pygame.Surface((WIDTH,HEIGHT))
	surface.fill(BACKGROUND)
	def key(s):
		return -s.level
	game.spaces.sort(key=key)
	for s in game.spaces:
		render_space(surface,s,game)
	render_builder(surface, game.builder, game)
	return surface
