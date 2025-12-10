import pygame
from configuracao import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        # Inicializa o sprite do Pygame
        super().__init__(groups)
        self.image = pygame.Surface((64, 64)) 
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2() 
        self.speed = 5 
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    def move(self, speed):
        if self.direction.length_squared() != 0:
             # length_squared() é mais rápido que length() para checar se o vetor não é zero
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT
    def update(self):
        self.input()
        self.move(self.speed)
