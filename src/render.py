from conf import *

def project(r,scale):
	x = r.x
	y = r.y
	return (WIDTH/2+scale*x*CAMERA_CONSTANT_SCALE,HEIGHT/2-scale*y*CAMERA_CONSTANT_SCALE)

def render_space(surface,s):
	r = s.r
	neighbours = [Vector2(1/2,1/2),Vector2(1/2,-1/2),Vector2(-1/2,-1/2),Vector2(-1/2,1/2)]
	screen_points = [project(r+n*s.size,1) for n in neighbours]
	pygame.draw.polygon(surface,(100,100,100),screen_points,width=1)

def render_object(surface,o):
	r = o.r
	pygame.draw.aacircle(surface,(100,100,100),project(r,o.scale),CAMERA_CONSTANT_SCALE)

def render(game):
	surface = pygame.Surface((WIDTH,HEIGHT))
	surface.fill(BACKGROUND)
	for s in game.spaces:
		render_space(surface,s)
	render_object(surface, game.builder)
	return surface
