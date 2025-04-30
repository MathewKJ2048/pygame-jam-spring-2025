from conf import *
from game import *
from render import *


def init_game():
	game = Game()
	return game

def play():
	pygame.init()
	screen = pygame.display.set_mode([WIDTH, HEIGHT])
	game = init_game()
	while game.running:
		dt = CLOCK.tick(MAX_FRAME_RATE)/1000

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.exit()
			
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					log("press")
					game.expand()
				if event.key == pygame.K_b:
					game.place_bug()
				if event.key == pygame.K_e:
					game.place_engine()
				if event.key == pygame.K_t:
					game.place_tower()
				if event.key == pygame.K_h:
					game.place_high_tower()
			
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
		log("number of spaces",len(game.spaces))

		log("framerate:",round(1/dt))
		game.evolve(dt)
		screen.blit(render(game),(0,0))
		pygame.display.flip()
		if DEBUG:
			print(get_debug_transcript())


play()