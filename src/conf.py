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

pygame.init()
pygame.display.set_caption(NAME)



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
		print(type(diff))
		diff_mag = abs(diff)
	else:
		diff_mag = diff.length()
	if diff_mag<=change:
		return target
	return current + (change*diff/diff_mag)


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

