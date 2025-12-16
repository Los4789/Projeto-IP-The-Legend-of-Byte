import pygame, sys
from configuracao import *
from level import Level
class Game:
    def __init__(self):
        pygame.mixer.init() 
        pygame.init()
        self.Screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.DisplaySurface = pygame.display.get_surface()
        pygame.display.set_caption('The Legend of Byte')
        self.Clock = pygame.time.Clock()
        self.MusicGame = 'music/Chiptune Original.mp3'
        self.MusicGameOver = 'music/game_over_music.ogg'
        self.StartGame()
        self.GameOverSurf = pygame.image.load('graphics/game_over_screen.png').convert_alpha()
        self.GameOverRect = self.GameOverSurf.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.Font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 2) 
    def StartGame(self):
        self.Level = Level(self.Screen)
        self.GameDuration = 15000 
        self.StartTime = pygame.time.get_ticks()
        self.GameActive = True
        self.FinalScoreData = None
        self.PlayMusic(self.MusicGame, -1, 0.5)
        pygame.event.clear()
    def PlayMusic(self, Path, Loops=-1, Volume=0.5):
        pygame.mixer.music.load(Path)
        pygame.mixer.music.play(Loops)
        pygame.mixer.music.set_volume(Volume)
        print(f"Tocando música: {Path}")
    def Run(self):
        while True:
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if Event.type == ADD_TIME_EVENT:
                    if self.GameActive: 
                        self.StartTime += Event.amount
                if Event.type == pygame.KEYDOWN:
                    if not self.GameActive:
                        if Event.key == pygame.K_r:
                            self.StartGame()
                        if Event.key == pygame.K_s:
                            pygame.mixer.music.stop()
                            pygame.quit()
                            sys.exit()
            if self.GameActive:
                CurrentTime = pygame.time.get_ticks()
                TimeLeftMs = self.GameDuration - (CurrentTime - self.StartTime)
                if TimeLeftMs <= 0:
                    TimeLeftMs = 0
                    self.GameActive = False 
                    self.FinalScoreData = self.Level.Score 
                    pygame.mixer.music.stop() 
                    self.PlayMusic(self.MusicGameOver, -1, 0.6) 
                self.Screen.fill('black')
                self.Level.Run(int(TimeLeftMs / 1000))
            else:
                if self.GameOverSurf:
                    self.Screen.blit(self.GameOverSurf, self.GameOverRect)
                else:
                    self.Screen.fill('gray')  
                if self.FinalScoreData:
                    TotalScore = sum(self.FinalScoreData.values())
                    ScoreText = f'Score Final: {TotalScore}'
                    ScoreSurface = self.Font.render(ScoreText, True, TEXT_COLOR)
                    ScoreRect = ScoreSurface.get_rect(topright=(WIDTH - 10, 10))
                    pygame.draw.rect(self.Screen, 'black', ScoreRect.inflate(10, 10), 0, 5)
                    self.Screen.blit(ScoreSurface, ScoreRect)
                RestartText = 'R = Recomeçar'
                RestartSurface = self.Font.render(RestartText, True, TEXT_COLOR)
                RestartRect = RestartSurface.get_rect(bottomleft=(5, HEIGHT - 5))
                QuitText = 'S = Sair'
                QuitSurface = self.Font.render(QuitText, True, TEXT_COLOR)
                QuitRect = QuitSurface.get_rect(topleft=(5, 5))
                pygame.draw.rect(self.Screen, 'black', QuitRect.inflate(10, 10), 0, 5)
                self.Screen.blit(QuitSurface, QuitRect)
                pygame.draw.rect(self.Screen, 'black', RestartRect.inflate(10, 10), 0, 5)
                self.Screen.blit(RestartSurface, RestartRect)
            pygame.display.update()
            self.Clock.tick(FPS)
if __name__ == '__main__':
    MyGame = Game()
    MyGame.Run()
