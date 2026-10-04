import pygame
import random
import math
import os
from ..location import Location, LocationRules


class CrossroadsLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(64, 224, 208)  # Turquoise color
        )
        self.obstacles = []
        self.background = pygame.Surface((width, height))
        self.background.fill((0, 0, 0))
        self.portal_rect = pygame.Rect(width - 40, height - 40, 30, 30)
        self.portal_active = False

        # Creepy bush (sprite that appears at random places and drifts slowly)
        bush_path = os.path.join(os.path.dirname(__file__), "..", "assets", "BG_images", "creepy_bush.png")
        self.bush_size = 120
        try:
            bush = pygame.image.load(bush_path).convert_alpha()
            self.bush_image = pygame.transform.scale(bush, (self.bush_size, self.bush_size))
        except Exception as e:
            print(f"Error loading creepy bush: {e}")
            self.bush_image = None
        self.bush_rect = pygame.Rect(0, 0, self.bush_size, self.bush_size)
        self.bush_active = False
        self.bush_vx = 0.0
        self.bush_vy = 0.0
        self.bush_expire_time = 0
        self.next_bush_direction_change = 0
        self.curse_active = False
        self.curse_accum = 0.0
        self.next_bush_time = pygame.time.get_ticks() + random.randint(35000, 55000)

        # Enhanced flicker variables
        self.light_on = False
        self.flicker_intensity = 0.0
        self.next_toggle_ms = pygame.time.get_ticks() + random.randint(2000, 6000)
        self.flicker_toggles_left = 0

    def update(self, dt):
        super().update(dt)
        current_time = pygame.time.get_ticks()

        prev_light_on = self.light_on

        if self.flicker_toggles_left > 0:
            if current_time >= self.next_toggle_ms:
                self.light_on = not self.light_on
                self.flicker_toggles_left -= 1
                if self.light_on:
                    self.flicker_intensity = random.uniform(0.4, 1.0)
                    self.next_toggle_ms = current_time + random.randint(30, 140)
                else:
                    self.flicker_intensity = 0.0
                    self.next_toggle_ms = current_time + random.randint(20, 120)
                if self.flicker_toggles_left == 0:
                    self.light_on = False
                    self.flicker_intensity = 0.0
                    self.next_toggle_ms = current_time + random.randint(2000, 6000)
        else:
            if current_time >= self.next_toggle_ms:
                self.flicker_toggles_left = random.randint(4, 14)
                self.light_on = True
                self.flicker_intensity = random.uniform(0.4, 1.0)
                self.next_toggle_ms = current_time + random.randint(30, 140)

        # Spawn creepy bush: once every 35-55s on a light-on rising edge
        if self.light_on and not prev_light_on:
            if not self.bush_active and current_time >= self.next_bush_time:
                self._spawn_bush()

        # Bush drifts slowly and disappears by itself after 10-20s
        if self.bush_active:
            self.bush_rect.x += self.bush_vx * dt
            self.bush_rect.y += self.bush_vy * dt

            if self.bush_rect.left < 0:
                self.bush_rect.left = 0
                self.bush_vx = abs(self.bush_vx)
            elif self.bush_rect.right > self.width:
                self.bush_rect.right = self.width
                self.bush_vx = -abs(self.bush_vx)
            if self.bush_rect.top < 0:
                self.bush_rect.top = 0
                self.bush_vy = abs(self.bush_vy)
            elif self.bush_rect.bottom > self.height:
                self.bush_rect.bottom = self.height
                self.bush_vy = -abs(self.bush_vy)

            if current_time >= self.next_bush_direction_change:
                speed = random.uniform(30, 60)
                angle = random.uniform(0, 2 * math.pi)
                self.bush_vx = speed * math.cos(angle)
                self.bush_vy = speed * math.sin(angle)
                self.next_bush_direction_change = current_time + random.randint(1000, 3000)

            if current_time >= self.bush_expire_time:
                self.bush_active = False
                self.next_bush_time = current_time + random.randint(35000, 55000)

        return self.light_on

    def _spawn_bush(self):
        max_x = self.width - self.bush_size
        max_y = self.height - self.bush_size
        self.bush_rect.topleft = (random.randint(0, max_x), random.randint(0, max_y))
        speed = random.uniform(30, 60)
        angle = random.uniform(0, 2 * math.pi)
        self.bush_vx = speed * math.cos(angle)
        self.bush_vy = speed * math.sin(angle)
        self.bush_expire_time = pygame.time.get_ticks() + random.randint(10000, 20000)
        self.next_bush_direction_change = pygame.time.get_ticks() + random.randint(1000, 3000)
        self.bush_active = True

    def check_collisions(self, snake):
        if self.bush_active:
            for segment in snake.body:
                segment_rect = pygame.Rect(segment[0], segment[1], snake.block_size, snake.block_size)
                if segment_rect.colliderect(self.bush_rect):
                    self.curse_active = True
                    self.bush_active = False
                    self.next_bush_time = pygame.time.get_ticks() + random.randint(35000, 55000)
                    break
        return False

    def draw(self, surface):
        surface.fill((0, 0, 0))
        if self.light_on:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            alpha = int(255 * self.flicker_intensity)
            overlay.fill((255, 255, 255, alpha))
            surface.blit(overlay, (0, 0))

        if self.bush_active and self.light_on and self.bush_image:
            surface.blit(self.bush_image, self.bush_rect.topleft)

        return self.light_on