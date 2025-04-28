from conf import *

def project(r,scale):
	x = r.x
	y = r.y
	return (WIDTH/2+scale*x*100,HEIGHT/2-scale*y)

def render_space(surface,s):
	r = s.r
	neighbours = [Vector2(1/2,1/2),Vector2(1/2,-1/2),Vector2(-1/2,1/2),Vector2(-1/2,-1/2)]
	screen_points = [project(r+n*s.size,game.scale) for n in neighbours]
	pygame.draw.polygon(surface,(100,100,100),screen_points)

def render(game):
	surface = pygame.Surface((WIDTH,HEIGHT))
	surface.fill(BACKGROUND)
	for s in game.spaces:
		render_space(surface,s)
	return surface
