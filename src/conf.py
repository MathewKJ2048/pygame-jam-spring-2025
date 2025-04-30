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

SUBDIVISION = 3

CAMERA_CONSTANT_SCALE = 100

I = Vector2(1,0)
J = Vector2(0,1)

I3 = Vector3(1,0,0)
J3 = Vector3(0,1,0)
K3 = Vector3(0,0,1)

VELOCITY = 8

def unit_vector(theta):
	return math.cos(theta)*I + math.sin(theta)*J

def make_pair_list(base_list):
	pair_list = []
	for i in range(len(base_list)):
		pair_list.append((base_list[i],base_list[(i+1)%len(base_list)]))
	return pair_list