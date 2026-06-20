import pygame
import random
import math
from typing import List

class Particle:
    """Single particle for explosion effects"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = (
            255, 105, 180  # Bright pink
        )  # Flower bush explosion color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 3)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = random.randint(20, 40)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class ParticleSystem:
    """Manages all active particles"""
    def __init__(self):
        self.particles: List[Particle] = []
    
    def add_explosion(self, x, y, count=30):
        """Create explosion particles at given position"""
        for _ in range(count):
            self.particles.append(Particle(x, y))
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface)