import math
import random

import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.shape = self.generate_shape()

    def generate_shape(self):
        num_vertices = random.randint(8, 12)
        shape = []
        for i in range(num_vertices):
            angle = (i / num_vertices) * 2 * math.pi
            distance = self.radius * random.uniform(0.8, 1.2)
            point = pygame.Vector2(
                distance * math.cos(angle), distance * math.sin(angle)
            )
            shape.append(point)
        return shape

    def draw(self, screen):
        points = [p + self.position for p in self.shape]
        pygame.draw.polygon(screen, "white", points, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        angle = random.uniform(20, 50)

        new_angle1 = self.velocity.rotate(angle)
        new_angle2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        new_asteroid1.velocity = new_angle1 * 1.2
        new_asteroid2.velocity = new_angle2 * 1.2
