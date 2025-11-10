import pygame
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.shot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_timer <= 0:
            self.shot_timer = PLAYER_SHOOT_COOLDOWN

            new_shot = Shot(self.position.x, self.position.y)
            new_shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            )

    def collides(self, other):
        # http://www.jeffreythompson.org/collision-detection/tri-circle.php
        a, b, c = self.triangle()

        if self.is_point_in_triangle(other.position, a, b, c):
            return True

        for p1, p2 in [(a, b), (b, c), (c, a)]:
            closest_point = self.closest_point_on_segment(other.position, p1, p2)
            if other.position.distance_to(closest_point) <= other.radius:
                return True
        return False

    def is_point_in_triangle(self, pt, v1, v2, v3):
        # https://stackoverflow.com/a/13305589/1792519
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(pt, v1, v2)
        d2 = sign(pt, v2, v3)
        d3 = sign(pt, v3, v1)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    def closest_point_on_segment(self, p, a, b):
        # https://stackoverflow.com/a/1501725/1792519
        ap = p - a
        ab = b - a
        ab2 = ab.x * ab.x + ab.y * ab.y
        ap_dot_ab = ap.x * ab.x + ap.y * ab.y
        t = ap_dot_ab / ab2
        t = max(0, min(1, t))
        return a + ab * t
