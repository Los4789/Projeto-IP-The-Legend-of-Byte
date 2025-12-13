import pygame
from tile import Tile 
from ui import UI
from coletaveis import Coletavel
from player import Player
from configuracao import *
# Camera
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        # Fundo para ajudar a visualizar o movimento da câmera
        self.floor_surf = pygame.Surface((WIDTH * 2, HEIGHT * 2)) # Um grande fundo preto
        self.floor_surf.fill('black')
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h
        # fundo com offset
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
class Level:
    def __init__(self, surface):
        self.display_surface = surface 
        self.visible_sprites = CameraGroup() 
        self.collectible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group() 
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
        
        self.create_map()
        self.score = {
            'moeda': 0,
            'estrela': 0,
            'joia': 0
        }
        self.ui = UI()
    def create_map(self):
        # Iterar sobre o mapa definido acima
        for row_index, row in enumerate(self.game_map):
            for col_index, cell in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if cell == 'X':
                    # Crie Tiles para os limites e adicione aos grupos corretos
                    # Nota: Certifique-se que a classe Tile tenha sido criada conforme instruído anteriormente
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
            collectible.kill() # Remove o item do jogo e dos grupos
            print(f"Coletou {collectible.type}! Score atual: {self.score}")
                
    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player) 
        self.check_collisions() 
        self.ui.show_score(self.score)
