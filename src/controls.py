from conf import *

def process_pressed_keys(game):
	pressed_keys = pygame.key.get_pressed()
	game.builder.v = Vector2(0,0)
	game.camera_omega = 0
	if pressed_keys[pygame.K_COMMA]:
		game.camera_omega += 1
	if pressed_keys[pygame.K_PERIOD]:
		game.camera_omega -= 1
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
	if event.key == pygame.K_v:
		game.place_battery()
	if event.key == pygame.K_w:
		game.place_warper()
	if event.key == pygame.K_c:
		game.place_cannon()
	if event.key == pygame.K_q:
		game.remove_selected_object()
	if event.key == pygame.K_z:
		if get_MUSIC():
			pygame.mixer.music.fadeout(1000)
		else:
			play_music()
		toggle_MUSIC()
	if event.key == pygame.K_x:
		toggle_SFX()
	if event.key == pygame.K_p:
		game.paused = not game.paused
	if event.key == pygame.K_m:
		game.minimap = not game.minimap