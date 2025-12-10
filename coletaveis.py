import pygame
class Coletavel(pygame.sprite.Sprite):
    def __init__(self, pos, type, groups):
        super().__init__(groups)
        self.type = type # 'moeda', 'estrela', 'joia'
        # Substituir por gráficos de sprites depois
        # Exemplo: self.image = pygame.image.load(f'graphics/{type}.png').convert_alpha()
        # Por enquanto é uma superfice temporária:
        if self.type == 'moeda':
            self.image = pygame.Surface((32, 32))
            self.image.fill('yellow')
        elif self.type == 'estrela':
            self.image = pygame.Surface((32, 32))
            self.image.fill('white')
        elif self.type == 'joia':
            self.image = pygame.Surface((32, 32))
            self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
