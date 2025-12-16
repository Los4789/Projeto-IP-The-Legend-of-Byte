import pygame, sys
from configuracao import *
from level import Level
pg = pygame
class Game:
    def __init__(self):
        pg.mixer.init() 
        pg.init()
        self.Screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.DisplaySurface = pg.display.get_surface()
        pg.display.set_caption('The Legend of Byte')
        self.Clock = pg.time.Clock()
        self.MusicGame = 'music/Chiptune Original.mp3'
        self.MusicGameOver = 'music/game_over_music.ogg'
        self.StartGame()
        self.GameOverSurf = pg.image.load('graphics/game_over_screen.png').convert_alpha()
        self.GameOverRect = self.GameOverSurf.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.Font = pg.font.Font(UI_FONT, UI_FONT_SIZE * 2) 
    def StartGame(self):
        self.Level = Level(self.Screen)
        self.GameDuration = 15000 
        self.StartTime = pg.time.get_ticks()
        self.GameActive = True
        self.FinalScoreData = None
        self.PlayMusic(self.MusicGame, -1, 0.5)
        pg.event.clear()
    def PlayMusic(self, Path, Loops=-1, Volume=0.5):
        pg.mixer.music.load(Path)
        pg.mixer.music.play(Loops)
        pg.mixer.music.set_volume(Volume)
        print(f"Tocando música: {Path}")
    def Run(self):
        while True:
            for Event in pg.event.get():
                if Event.type == pg.QUIT:
                    pg.mixer.music.stop()
                    pg.quit()
                    sys.exit()
                if Event.type == ADD_TIME_EVENT:
                    if self.GameActive: 
                        self.StartTime += Event.amount
                if Event.type == pg.KEYDOWN:
                    if not self.GameActive:
                        if Event.key == pg.K_r:
                            self.StartGame()
                        if Event.key == pg.K_ESCAPE:
                            pg.mixer.music.stop()
                            pg.quit()
                            sys.exit()
            if self.GameActive:
                CurrentTime = pg.time.get_ticks()
                TimeLeftMs = self.GameDuration - (CurrentTime - self.StartTime)
                if TimeLeftMs <= 0:
                    TimeLeftMs = 0
                    self.GameActive = False 
                    self.FinalScoreData = self.Level.Score 
                    pg.mixer.music.stop() 
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
                    pg.draw.rect(self.Screen, 'black', ScoreRect.inflate(10, 10), 0, 5)
                    self.Screen.blit(ScoreSurface, ScoreRect)
                RestartText = 'R = Recomeçar'
                RestartSurface = self.Font.render(RestartText, True, TEXT_COLOR)
                RestartRect = RestartSurface.get_rect(bottomleft=(5, HEIGHT - 5))
                QuitText = 'Esc = Sair'
                QuitSurface = self.Font.render(QuitText, True, TEXT_COLOR)
                QuitRect = QuitSurface.get_rect(topleft=(5, 5))
                pg.draw.rect(self.Screen, 'black', QuitRect.inflate(10, 10), 0, 5)
                self.Screen.blit(QuitSurface, QuitRect)
                pg.draw.rect(self.Screen, 'black', RestartRect.inflate(10, 10), 0, 5)
                self.Screen.blit(RestartSurface, RestartRect)
            pg.display.update()
            self.Clock.tick(FPS)
#####

pg.init()
tela = pg.display.set_mode((WIDTH, HEIGHT))
telaa = tela.get_rect(); centro = telaa.center
pg.display.set_caption("jogo")
main_menu = True; opacidade = 255
mascara = pg.Surface((1280, 720)); mascara.fill((255,255,255))

def animar_abrir():
    #animação do apertar START!
    iterador = 0
    for x in range(500):
        iterador += 3
        pg.draw.rect(tela, (255,255,255), (centro[0]-(iterador//2), centro[1]-(iterador//2),iterador,iterador))
        pg.display.update()

tela_inicial = pg.image.load('fundo.jpg').convert()
botao = pg.image.load('botao.png').convert_alpha()
botao = pg.transform.scale(botao, (200,160))
area_clicavel = pg.draw.rect(tela, (0,0,0), (centro[0]-65, centro[1]-33, 130, 56))

while main_menu:
    tela.blit(tela_inicial, (0, 0))
    tela.blit(botao, (centro[0]-100, centro[1]-85))
    #só coloquei o lance de poder sair apertando "ESC"
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if area_clicavel.collidepoint(event.pos):
                animar_abrir()
                main_menu = False
                if __name__ == '__main__':
                    MyGame = Game()
                    MyGame.Run()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                animar_abrir()
                main_menu = False
                if __name__ == '__main__':
                    MyGame = Game()
                    MyGame.Run()
    pg.display.update()
while True: #daqui para baixo é uma protése para o código principal
    tela.fill((255,0,0))#  <--------------- isso é a tela do jogo
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
    if opacidade > 0:
        opacidade -= 1
    else:
        opacidade = 0
    mascara.set_alpha(opacidade)
    tela.blit(mascara, (0,0))
    pg.display.update()
