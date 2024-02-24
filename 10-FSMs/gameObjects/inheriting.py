from . import Kirby, Controllable
import pygame
from utils import vec, magnitude, scale
import numpy as np


class Inheriting(Controllable):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(0, 0)

    def update(self, seconds, map=None):
        super().update(seconds, map)
        pass
