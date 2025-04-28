import time
import pygame
from pygame import Vector2
import math
import random
from colors import *

CLOCK = pygame.time.Clock()

MAX_FRAME_RATE = 60

DEBUG = True

WIDTH = 1200
HEIGHT = 800

SUBDIVISION = 4

CAMERA_CONSTANT_SCALE = 10