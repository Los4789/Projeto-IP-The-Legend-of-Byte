import pygame
from configuracao import *
from support import import_folder
import os
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.base_path = 'graphics/objects/player/'
        self.import_assets()
        self.status = 'south_idle' # Estado inicial: idle para baixo
        self.frame_index = 0
        self.animation_speed = 0.15 
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, -20) 
        self.direction = pygame.math.Vector2() 
        self.speed = 8 
        #Lógica de Boost
        self.original_speed = 8
        self.boost_active = False
        self.boost_start_time = 0
        self.boost_duration = 5000 # 5 segundos
        self.obstacle_sprites = obstacle_sprites
    def activate_speed_boost(self):
        if not self.boost_active:
            self.boost_active = True
            self.speed = self.original_speed * 1.5 # Aumenta 50%
            self.boost_start_time = pygame.time.get_ticks()
    def import_assets(self):
        self.animations = {}
        idle_directions = ['north', 'east', 'west', 'south']
        for direction in idle_directions:
            path = os.path.join(self.base_path, f'{direction}.png')
            image_surf = pygame.image.load(path).convert_alpha()
            self.animations[f'{direction}_idle'] = [image_surf]
        animation_directions = ['east', 'west', 'north', 'south']
        for direction in animation_directions:
            folder_path = os.path.join(self.base_path, 'animations', 'walking-8-frames', direction)
            self.animations[f'{direction}_run'] = import_folder(folder_path)
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect.center = self.hitbox.center
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.y = 0
        self.direction.x = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'north_run'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'south_run'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'east_run'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'west_run'
        if self.direction.x == 0 and self.direction.y == 0:
            if not self.status.endswith('_idle'):
                self.status = self.status.replace('_run', '_idle')
                self.frame_index = 0
    def move(self, speed):
        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center 
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom
    def update(self):
        self.input()
        self.move(self.speed)
        self.animate()
        if self.boost_active:
            if pygame.time.get_ticks() - self.boost_start_time >= self.boost_duration:
                self.boost_active = False
                self.speed = self.original_speed
