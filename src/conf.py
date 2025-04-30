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

SUBDIVISION = 4

CAMERA_CONSTANT_SCALE = 100

I = Vector2(1,0)
J = Vector2(0,1)

VELOCITY = 8

def unit_vector(theta):
	return math.cos(theta)*I + math.sin(theta)*J