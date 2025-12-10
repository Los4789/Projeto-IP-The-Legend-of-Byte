class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        
        self.create_map()
        
        # Dados do Placar
        self.score = {
            'moeda': 0,
            'estrela': 0,
            'joia': 0
        }
        
        # Interface do usuário
        self.ui = UI()

    def create_map(self):
        # Criação de itens colecionáveis de exemplo no mapa
        # Substitua por sua lógica de mapa real
        Coletavel((200, 300), 'moeda', [self.visible_sprites, self.collectible_sprites])
        Coletavel((400, 300), 'estrela', [self.visible_sprites, self.collectible_sprites])
        Coletavel((600, 300), 'joia', [self.visible_sprites, self.collectible_sprites])
        # self.player = Player((WIDTH/2, HEIGHT/2), [self.visible_sprites])

    def check_collisions(self):
        # Lógica de colisão: verifica se o player colidiu com algum item colecionável
        for collectible in self.collectible_sprites:
            # if collectible.rect.colliderect(self.player.rect): # Ative quando tiver a classe Player
            #     self.score[collectible.type] += 1
            #     collectible.kill() # Remove o item do jogo e dos grupos
            #     print(f"Coletou {collectible.type}! Score atual: {self.score}")
            pass # Remover este 'pass' quando ativar o código acima
    def run(self):
        # self.visible_sprites.draw(self.display_surface) # Desenha sprites visíveis
        self.visible_sprites.update()
        # self.check_collisions() # Ative quando tiver a classe Player
        self.ui.show_score(self.score) # Mostra o placar
