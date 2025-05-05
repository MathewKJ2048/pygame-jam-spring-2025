import time
import pygame
from pygame import Vector2
from pygame import Vector3
import math
import random
import os
from colors import *

NAME = "Grid Surge"
WIDTH = 1200
HEIGHT = 800

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption(NAME)
icon = pygame.image.load("assets/icon.ico")
pygame.display.set_icon(icon)

MUSIC = True
SFX = True
def get_MUSIC():
	global MUSIC
	return MUSIC
def toggle_MUSIC():
	global MUSIC
	MUSIC = not MUSIC
def get_SFX():
	global SFX
	return SFX
def toggle_SFX():
	global SFX
	SFX = not SFX

pygame.mixer.music.load("./assets/game_jam_music.wav")
def play_music():
	pygame.mixer.music.play(-1)

warp_sound = pygame.mixer.Sound('./assets/warp.wav')
construction_sound = pygame.mixer.Sound("./assets/construction.wav")
destruction_sound = pygame.mixer.Sound("./assets/destruction.wav")
laser_sound = pygame.mixer.Sound("./assets/laser.wav")
laser_sound.set_volume(0.2)
destruction_sound.set_volume(0.5)

def play_sound(s):
	global SFX
	if SFX:
		s.play()


MINI_WIDTH = WIDTH/4
MINI_HEIGHT = HEIGHT/4
MINI_SCALE = 4
BLIP_RADIUS = 2


CLOCK = pygame.time.Clock()



debug_transcript = {}
def log(key,value=None):
	global debug_transcript
	if value:
		debug_transcript[key] = str(value)
	else:
		debug_transcript[key] = ""
def get_debug_transcript():
	global debug_transcript
	return debug_transcript

MAX_FRAME_RATE = 60

DEBUG = True



DUAL = 0
INPUT = 1
OUTPUT = 2

ERROR_X = WIDTH
ERROR_Y = HEIGHT
XMIN = -ERROR_X
YMIN = -ERROR_Y
XMAX = WIDTH+ERROR_X
YMAX = HEIGHT+ERROR_Y

BUILDER_ANGULAR_VELOCITY = 1
GAIT = 0.4

SUBDIVISION = 5

CAMERA_CONSTANT_SCALE = 100

I = Vector2(1,0)
J = Vector2(0,1)

I3 = Vector3(1,0,0)
J3 = Vector3(0,1,0)
K3 = Vector3(0,0,1)

VELOCITY = 8

def unit_vector(theta):
	return math.cos(theta)*I + math.sin(theta)*J

def unit_vector3(theta):
	return math.cos(theta)*I3 + math.sin(theta)*J3


I_transform = unit_vector(math.pi/6)
J_transform = unit_vector(5*math.pi/6)
K_transform = unit_vector(math.pi/2)

def make_pair_list(base_list):
	return [(base_list[i],base_list[(i+1)%len(base_list)]) for i in range(len(base_list))]

def interweave(l1,l2,offset=0):
	N = len(l1)
	offset = offset+2*N
	return [(l1[i],l2[(i+offset)%N]) for i in range(N)]

def join(l,u):
	return [(t,u) for t in l]

def lerp_approach(current,target,rate,dt): # returns new target
	change = rate*dt
	diff =  (target-current)
	log("diff_type",type(diff))
	if type(diff) in [float,int]:
		diff_mag = abs(diff)
	else:
		diff_mag = diff.length()
	if diff_mag<=change:
		return target
	return current + (change*diff/diff_mag)

def set_max(v,maximum):
	l = v.length()
	if l == 0:
		return v
	return v.normalize()*min(l,maximum)

def normalize_with_0(v):
	if v.length() == 0:
		return v
	return v.normalize()

def solve(L1,L2,P,O):
	P = P-O
	RAD = Vector3(P.x,P.y,0)
	AZ = Vector3(0,0,P.z)
	x0, y0 = RAD.length(), AZ.length()

	Lsq = x0*x0+y0*y0
	L = math.sqrt(Lsq)
	L1sq = L1*L1
	L2sq = L2*L2
	p = (Lsq+L1sq-L2sq)/(2*L)
	h = math.sqrt(abs(L1sq-p*p))

	p_cap = P.normalize()
	h_cap = RAD*y0 - AZ*x0
	answer = O+p*p_cap+h*h_cap
	return answer

def rotate_xy(v,angle):
	l = Vector2(v.x,v.y).length()
	if l == 0:
		return v
	t = math.atan2(v.y,v.x)
	return unit_vector3(t+angle)*l + v.z*K3

