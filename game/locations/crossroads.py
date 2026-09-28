import pygame
import random
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

        # Enhanced flicker variables
        self.light_on = False
        self.flicker_intensity = 0.0
        self.next_toggle_ms = pygame.time.get_ticks() + random.randint(2000, 6000)
        self.flicker_toggles_left = 0

    def update(self, dt):
        super().update(dt)
        current_time = pygame.time.get_ticks()

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

        return self.light_on

    def draw(self, surface):
        surface.fill((0, 0, 0))
        if self.light_on:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            alpha = int(255 * self.flicker_intensity)
            overlay.fill((255, 255, 255, alpha))
            surface.blit(overlay, (0, 0))

        if self.portal_active:
            pygame.draw.rect(surface, (255, 0, 255), self.portal_rect)

        return self.light_on