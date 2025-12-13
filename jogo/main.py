import pygame, sys
from configuracao import *
from level import Level
class Game:
    def __init__(self):
        pygame.mixer.init() 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_surface = pygame.display.get_surface()
        pygame.display.set_caption('The Legend of Byte')
        self.clock = pygame.time.Clock()
        self.music_game = 'music/OPRG.ogg'
        self.music_game_over = 'music/game_over_music.ogg'
        self.start_game()
        try:
            self.game_over_surf = pygame.image.load('graphics/game_over_screen.png').convert_alpha()
            self.game_over_rect = self.game_over_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de Game Over: {e}")
            self.game_over_surf = None
        try:
            self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 2) 
        except FileNotFoundError:
            print(f"Fonte {UI_FONT} não encontrada, usando fonte padrão.")
            self.font = pygame.font.Font(None, UI_FONT_SIZE * 2)
    def start_game(self):
        # Método para iniciar/reiniciar o jogo
        self.level = Level(self.screen)
        self.game_duration = 15000 
        self.start_time = pygame.time.get_ticks()
        self.game_active = True
        self.final_score_data = None
        self.play_music(self.music_game, -1, 0.5)
        pygame.event.clear()
    def play_music(self, path, loops=-1, volume=0.5):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops)
            pygame.mixer.music.set_volume(volume)
            print(f"Tocando música: {path}")
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar música {path}: {e}")
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == ADD_TIME_EVENT:
                    # Só adiciona tempo se o jogo estiver ativo
                    if self.game_active: 
                        self.start_time += event.amount
                if event.type == pygame.KEYDOWN:
                    if not self.game_active:
                        if event.key == pygame.K_r: # Pressionou 'R' para Reiniciar
                            self.start_game()
                        if event.key == pygame.K_q: # Pressionou 'Q' para Sair
                            pygame.mixer.music.stop()
                            pygame.quit()
                            sys.exit()
            if self.game_active:
                current_time = pygame.time.get_ticks()
                time_left_ms = self.game_duration - (current_time - self.start_time)
                if time_left_ms <= 0:
                    time_left_ms = 0
                    self.game_active = False 
                    self.final_score_data = self.level.score 
                    pygame.mixer.music.stop() 
                    self.play_music(self.music_game_over, -1, 0.6) 

                self.screen.fill('black')
                self.level.run(int(time_left_ms / 1000))
            else:
                if self.game_over_surf:
                    self.screen.blit(self.game_over_surf, self.game_over_rect)
                else:
                    self.screen.fill('gray')  
                if self.final_score_data:
                    total_score = sum(self.final_score_data.values())
                    score_text = f'Score Final: {total_score}'
                    score_surface = self.font.render(score_text, True, TEXT_COLOR)
                    score_rect = score_surface.get_rect(topright=(WIDTH - 50, 50))
                    pygame.draw.rect(self.screen, 'black', score_rect.inflate(10, 10), 0, 5)
                    self.screen.blit(score_surface, score_rect)
            pygame.display.update()
            self.clock.tick(FPS)
if __name__ == '__main__':
    game = Game()
    game.run()
