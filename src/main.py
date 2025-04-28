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
			
		pressed_keys = pygame.key.get_pressed()

		game.log("framerate:",round(1/dt))
		game.update(dt)
		screen.blit(render(game),(0,0))
		pygame.display.flip()
		if DEBUG:
			print(game.debug_transcript)


play()