import pygame
from configuracao import *
class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
    def show_score(self, score_data):
        text_surface = self.font.render(
            f'Moedas: {score_data["moeda"]} | Estrelas: {score_data["estrela"]} | Joias: {score_data["joia"]}', 
            False, 
            TEXT_COLOR
        )
        text_rect = text_surface.get_rect(topleft = (20, 20))
        pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(10, 10), 0, 5)
        self.display_surface.blit(text_surface, text_rect)
