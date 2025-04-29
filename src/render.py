from conf import *

def project(r,game):
	x = r.x
	y = r.y
	return (WIDTH/2+game.scale*x*CAMERA_CONSTANT_SCALE,HEIGHT/2-game.scale*y*CAMERA_CONSTANT_SCALE)

def render_space(surface,s,game,color_override = None):
	r = s.r
	neighbours = [Vector2(1/2,1/2),Vector2(1/2,-1/2),Vector2(-1/2,-1/2),Vector2(-1/2,1/2)]
	screen_points = [project(r+n*s.size,game) for n in neighbours]
	color = MAGENTA
	if s.level % 2 == 1:
		color = CYAN
	if color_override:
		color = color_override
	pygame.draw.polygon(surface,color,screen_points,width=1)

def render_object(surface,o,game):
	r = o.r
	size = CAMERA_CONSTANT_SCALE/2 * game.scale * o.scale
	pygame.draw.aacircle(surface,(100,100,100),project(r,game),size)

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
