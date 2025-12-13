import pygame
from support import import_folder
import os
class Coletavel(pygame.sprite.Sprite):
    def __init__(self, pos, type, groups):
        super().__init__(groups)
        self.type = type # 'moeda', 'estrela', 'joia'
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.10 # Velocidade de animação para os itens
        # A imagem inicial é o primeiro frame da animação correspondente ao tipo
        self.image = self.animations[self.type][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
    def import_assets(self):
        self.animations = {}
        base_path = 'graphics/objects/'
        # Mapeamento
        folder_mapping = {
            'moeda': 'coin',
            'estrela': 'star',
            'joia': 'diamond'
        }
        folder_name = folder_mapping[self.type]
        full_path = os.path.join(base_path, folder_name)
        self.animations[self.type] = import_folder(full_path)
    def animate(self):
        animation = self.animations[self.type]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
    def update(self):
        self.animate()
