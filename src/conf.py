import time
import pygame
from pygame import Vector2
from pygame import Vector3
import math
import random
import os
from colors import *

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

WIDTH = 1200
HEIGHT = 800

ERROR_X = WIDTH
ERROR_Y = HEIGHT
XMIN = -ERROR_X
YMIN = -ERROR_Y
XMAX = WIDTH+ERROR_X
YMAX = HEIGHT+ERROR_Y

BUILDER_ANGULAR_VELOCITY = 1
GAIT = 0.5

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
	pair_list = []
	for i in range(len(base_list)):
		pair_list.append((base_list[i],base_list[(i+1)%len(base_list)]))
	return pair_list

def lerp_approach(current,target,rate,dt): # returns new target
	change = rate*dt
	diff =  (target-current)
	if abs(diff)<=change:
		return target
	return current + (change*diff/abs(diff))