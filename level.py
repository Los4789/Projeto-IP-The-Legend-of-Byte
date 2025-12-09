import pygame
class Level:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.spritesvisiveis = pygame.sprite.Group()
    self.spritesobstaculos = pygame.sprite.Group()
  def run(self):
    pass
