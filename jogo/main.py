import pygame, sys
from configuracao import *
from level import Level
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('The Legend of Byte')
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)
        self.game_duration = 60000 # 60 segundos
        self.start_time = pygame.time.get_ticks()
        self.game_active = True
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ADD_TIME_EVENT:
                    # Tempo
                    self.start_time += event.amount 
            if self.game_active:
                current_time = pygame.time.get_ticks()
                time_left_ms = self.game_duration - (current_time - self.start_time)
                if time_left_ms <= 0:
                    time_left_ms = 0
                    self.game_active = False # Fim de jogo
                self.screen.fill('black')
                self.level.run(int(time_left_ms / 1000))
            else:
                self.screen.fill('gray') 
            pygame.display.update()
            self.clock.tick(FPS)
if __name__ == '__main__':
    game = Game()
    game.run()
    
