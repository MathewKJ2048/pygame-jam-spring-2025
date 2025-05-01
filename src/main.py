from conf import *
from game import *
from render import *

from shader_code import *


def init_game():
	game = Game()
	return game

def process_keydown_event(event,game):
	if event.key == pygame.K_s:
		game.expand()
	if event.key == pygame.K_b:
		game.place_bug()
	if event.key == pygame.K_e:
		game.place_engine()
	if event.key == pygame.K_t:
		game.place_tower()
	if event.key == pygame.K_h:
		game.place_high_tower()

def print_logs(dt):
	log("framerate:",round(1/dt))
	if DEBUG:
		print(get_debug_transcript())

def process_pressed_keys(game):
	pressed_keys = pygame.key.get_pressed()
	game.builder.v = Vector2(0,0)
	if pressed_keys[pygame.K_LEFT]:
		game.builder.v+=-I
	if pressed_keys[pygame.K_RIGHT]:
		game.builder.v+=I
	if pressed_keys[pygame.K_UP]:
		game.builder.v+=J
	if pressed_keys[pygame.K_DOWN]:
		game.builder.v+=-J
	if game.builder.v.length() > 0:
		game.builder.v = game.builder.v.normalize()
	game.builder.v*=VELOCITY




def play():
	game = init_game()
	screen = pygame.Surface((WIDTH, HEIGHT))

	while game.running:

		screen.blit(render(game),(0,0))

		dt = CLOCK.tick(MAX_FRAME_RATE)/1000

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.exit()
			elif event.type == pygame.KEYDOWN:
				process_keydown_event(event,game)
		process_pressed_keys(game)

		game.evolve(dt)


		frame_tex = surf_to_texture(screen)
		frame_tex.use(0)
		program['sceneTexture'] = 0
		render_object.render(mode=moderngl.TRIANGLE_STRIP)

		pygame.display.flip()
		print_logs(dt)

		frame_tex.release()



def main():
	play()

main()