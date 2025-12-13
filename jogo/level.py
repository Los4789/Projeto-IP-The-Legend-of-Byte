import pygame
from ui import UI
from coletaveis import Coletavel
from player import Player
from configuracao import *
from tile import Tile
class CameraGroup(pygame.sprite.Group):
    def __init__(self, map_width, map_height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size() // 2
        self.half_h = self.display_surface.get_size() // 2
        self.floor_surf_original = pygame.image.load('graphics/tilemap/ground.png').convert()
        num_tiles_x = int(map_width / self.floor_surf_original.get_width()) + 1
        num_tiles_y = int(map_height / self.floor_surf_original.get_height()) + 1
        self.floor_surf = pygame.Surface((num_tiles_x * self.floor_surf_original.get_width(), 
                                          num_tiles_y * self.floor_surf_original.get_height()))
        for x in range(num_tiles_x):
            for y in range(num_tiles_y):
                self.floor_surf.blit(self.floor_surf_original, (x * self.floor_surf_original.get_width(), 
                                                               y * self.floor_surf_original.get_height()))
                
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Level:
    def __init__(self, surface):
        self.display_surface = surface 
        
        self.game_map = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                         X',
            'X    C         E          X',
            'X                         X',
            'X              J          X',
            'X                         X',
            'X                         X',
            'XXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ]
        map_width = len(self.game_map[0]) * TILESIZE
        map_height = len(self.game_map) * TILESIZE

        # Use map_width e map_height na inicialização
        self.visible_sprites = CameraGroup(map_width, map_height) 
        
        self.collectible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group() 
        
        self.create_map()
        self.score = {
            'moeda': 0,
            'estrela': 0,
            'joia': 0
        }
        self.ui = UI()
        
    def create_map(self):
        for row_index, row in enumerate(self.game_map):
            for col_index, cell in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if cell == 'X':
                    # Tile precisa ser importada
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif cell == 'C':
                    Coletavel((x, y), 'moeda', [self.visible_sprites, self.collectible_sprites])
                elif cell == 'E':
                    Coletavel((x, y), 'estrela', [self.visible_sprites, self.collectible_sprites])
                elif cell == 'J':
                    Coletavel((x, y), 'joia', [self.visible_sprites, self.collectible_sprites])
                elif cell == 'P':
                    self.player = Player(
                        (x, y), 
                        [self.visible_sprites], 
                        self.obstacle_sprites # Passe o grupo de obstáculos aqui
                    )
        if not hasattr(self, 'player'):
             self.player = Player(
                        (WIDTH/2, HEIGHT/2), 
                        [self.visible_sprites], 
                        self.obstacle_sprites
                    )

    def check_collisions(self):
        for collectible in self.collectible_sprites:
          if collectible.rect.colliderect(self.player.hitbox): 
            self.score[collectible.type] += 1
            collectible.kill() 
            print(f"Coletou {collectible.type}! Score atual: {self.score}")
                
    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player) 
        self.check_collisions() 
        self.ui.show_score(self.score)
