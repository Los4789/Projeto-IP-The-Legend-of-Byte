import pygame
from ui import UI
from coletaveis import Coletavel
from player import Player
from configuracao import *
from tile import Tile
import random
from coletaveis import NOVO_TAMANHO_COLETAVEL

class CameraGroup(pygame.sprite.Group):
    def __init__(self, MapWidth, MapHeight):
        super().__init__()
        self.DisplaySurface = pygame.display.get_surface()
        self.Offset = pygame.math.Vector2()
        ScreenWidth, ScreenHeight = self.DisplaySurface.get_size()
        self.HalfW = ScreenWidth // 2
        self.HalfH = ScreenHeight // 2
        self.FloorSurfOriginal = pygame.image.load('graphics/tilemap/ground.png').convert()
        NumTilesX = int(MapWidth / self.FloorSurfOriginal.get_width()) + 1
        NumTilesY = int(MapHeight / self.FloorSurfOriginal.get_height()) + 1
        self.FloorSurf = pygame.Surface((NumTilesX * self.FloorSurfOriginal.get_width(), NumTilesY * self.FloorSurfOriginal.get_height()))
        for X in range(NumTilesX):
            for Y in range(NumTilesY):
                self.FloorSurf.blit(self.FloorSurfOriginal, (X * self.FloorSurfOriginal.get_width(), Y * self.FloorSurfOriginal.get_height()))
        self.FloorRect = self.FloorSurf.get_rect(topleft = (0, 0))
    def CustomDraw(self, Player):
        self.Offset.x = Player.rect.centerx - self.HalfW
        self.Offset.y = Player.rect.centery - self.HalfH
        FloorOffsetPos = self.FloorRect.topleft - self.Offset
        self.DisplaySurface.blit(self.FloorSurf, FloorOffsetPos)
        for Sprite in sorted(self.sprites(), key=lambda Sprite: Sprite.rect.centery):
            OffsetPos = Sprite.rect.topleft - self.Offset
            self.DisplaySurface.blit(Sprite.image, OffsetPos)
class Level:
    def __init__(self, Surface):
        self.DisplaySurface = Surface 
        self.GameMap = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                         X',
            'X    C         E          X',
            'X                         X',
            'X              J          X',
            'X                         X',
            'X                         X',
            'X                         X',
            'X                         X',
            'X                         X',
            'X                         X',
            'X                         X',
            'XXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ]
        MapWidth = len(self.GameMap[0]) * TILESIZE
        MapHeight = len(self.GameMap) * TILESIZE
        self.VisibleSprites = CameraGroup(MapWidth, MapHeight) 
        self.CollectibleSprites = pygame.sprite.Group()
        self.ObstacleSprites = pygame.sprite.Group() 
        
        self.CreateMap()
        self.Score = {
            'moeda': 0,
            'estrela': 0,
            'joia': 0
        }
        self.Ui = UI()
        self.Sfx = {
            'moeda': pygame.mixer.Sound('sound/coin.wav'),
            'estrela': pygame.mixer.Sound('sound/star.wav'),
            'joia': pygame.mixer.Sound('sound/diamond.wav')
        }
        
        for Sound in self.Sfx.values():
            Sound.set_volume(0.5)

    def CreateMap(self):
        for RowIndex, Row in enumerate(self.GameMap):
            for ColIndex, Cell in enumerate(Row):
                X = ColIndex * TILESIZE
                Y = RowIndex * TILESIZE
                if Cell == 'X':
                    Tile((X, Y), [self.VisibleSprites, self.ObstacleSprites])
                elif Cell == 'C':
                    Coletavel((X, Y), 'moeda', [self.VisibleSprites, self.CollectibleSprites])
                elif Cell == 'E':
                    Coletavel((X, Y), 'estrela', [self.VisibleSprites, self.CollectibleSprites])
                elif Cell == 'J':
                    Coletavel((X, Y), 'joia', [self.VisibleSprites, self.CollectibleSprites])
                elif Cell == 'P':
                    self.Player = Player(
                        (X, Y), 
                        [self.VisibleSprites], 
                        self.ObstacleSprites
                    )
        if not hasattr(self, 'Player'):
             self.Player = Player(
                        (WIDTH/2, HEIGHT/2), 
                        [self.VisibleSprites], 
                        self.ObstacleSprites
                    )

    def SpawnNewCollectible(self, CType):
        while True:
            X = random.randint(0, len(self.GameMap[0]) * TILESIZE - NOVO_TAMANHO_COLETAVEL)
            Y = random.randint(0, len(self.GameMap) * TILESIZE - NOVO_TAMANHO_COLETAVEL)
            TempRect = pygame.Rect(X, Y, NOVO_TAMANHO_COLETAVEL, NOVO_TAMANHO_COLETAVEL)
            CollisionFound = False
            for Sprite in self.ObstacleSprites:
                if Sprite.hitbox.colliderect(TempRect):
                    CollisionFound = True
                    break
            if not CollisionFound:
                Coletavel((X, Y), CType, [self.VisibleSprites, self.CollectibleSprites])
                break

    def CheckCollisions(self, TimeLeftSeconds):
        for Collectible in self.CollectibleSprites:
          if Collectible.rect.colliderect(self.Player.hitbox): 
            CType = Collectible.type
            if CType in self.Sfx:
                self.Sfx[CType].play()
            
            if CType == 'moeda':
                self.Score[CType] += ScoreDefault
                TimeEvent = pygame.event.Event(ADD_TIME_EVENT, {'amount': TIME_MOEDA_MS})
                pygame.event.post(TimeEvent)
            elif CType == 'estrela':
                 self.Score[CType] += ScoreDefault
                 self.Player.activate_speed_boost()
            elif CType == 'joia':
                self.Score[CType] += ScoreJoia
            else:
                self.Score[CType] += ScoreDefault
            
            Collectible.kill() 
            self.SpawnNewCollectible(CType)

    def Run(self, TimeLeftSeconds):
        self.VisibleSprites.update()
        self.VisibleSprites.CustomDraw(self.Player) 
        self.CheckCollisions(TimeLeftSeconds) 
        self.Ui.show_score(self.Score, TimeLeftSeconds)
