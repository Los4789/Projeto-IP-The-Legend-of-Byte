import pygame
from support import import_folder
import os
from configuracao import TILESIZE
NOVO_TAMANHO_COLETAVEL = TILESIZE * 2 
class Coletavel(pygame.sprite.Sprite):
    def __init__(self, pos, type, groups):
        super().__init__(groups)
        self.type = type 
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.10 
        self.image = self.animations[self.type][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
    def import_assets(self):
        self.animations = {}
        base_path = 'graphics/objects/'
        folder_mapping = {
            'moeda': 'coin',
            'estrela': 'star',
            'joia': 'diamond'
        }
        
        folder_name = folder_mapping[self.type]
        full_path = os.path.join(base_path, folder_name)
        original_frames = import_folder(full_path)
        resized_frames = []
        for frame in original_frames:
            resized_frame = pygame.transform.scale(frame, (NOVO_TAMANHO_COLETAVEL, NOVO_TAMANHO_COLETAVEL))
            resized_frames.append(resized_frame)
        self.animations[self.type] = resized_frames

    def animate(self):
        animation = self.animations[self.type]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def update(self):
        self.animate()
