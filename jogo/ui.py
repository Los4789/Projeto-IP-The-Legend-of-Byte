import pygame
from configuracao import *
from level import ScoreDefault, ScoreJoia

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
    def show_score(self, score_data, time_left_seconds):
        individual_counts_surface = self.font.render(
            f'Moedas: {score_data["moeda"]/ScoreDefault} | Estrelas: {score_data["estrela"]/ScoreDefault} | Joias: {score_data["joia"]/ScoreJoia}', 
            False, 
            TEXT_COLOR
        )
        individual_counts_rect = individual_counts_surface.get_rect(topleft = (20, 20))
        pygame.draw.rect(self.display_surface, 'black', individual_counts_rect.inflate(10, 10), 0, 5)
        self.display_surface.blit(individual_counts_surface, individual_counts_rect)
        total_score = sum(score_data.values()) # Soma todos os pontos
        total_score_surface = self.font.render(
            f'Score Total: {total_score}', 
            False, 
            TEXT_COLOR
        )
        total_score_rect = total_score_surface.get_rect(topleft = (20, 50))
        pygame.draw.rect(self.display_surface, 'black', total_score_rect.inflate(10, 10), 0, 5)
        self.display_surface.blit(total_score_surface, total_score_rect)
        minutes = int(time_left_seconds // 60)
        seconds = int(time_left_seconds % 60)
        time_text = f'Tempo: {minutes:02}:{seconds:02}'
        time_surface = self.font.render(
            time_text, 
            False, 
            TEXT_COLOR
        )
        time_rect = time_surface.get_rect(topright = (self.display_surface.get_width() - 20, 20))
        pygame.draw.rect(self.display_surface, 'black', time_rect.inflate(10, 10), 0, 5)
        self.display_surface.blit(time_surface, time_rect)
