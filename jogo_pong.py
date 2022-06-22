import pygame


pygame.init()
altura = 600
largura = 800
tamanhoJanela = (largura, altura)
janela = pygame.display.set_mode(tamanhoJanela)
pygame.display.set_caption('Pong, por Marco, Felipe e Matheus Rodrigues dos Santos')

branco = (255, 255, 255)
preto = (0, 0, 0)

larguraJogador , alturaJogador = 20, 100

class jogadores:
    cor = branco

    def __init__(self, x, y , larguraJogador, alturaJogador):
        self.x = x
        self.y =y
        self.larguraJogador = larguraJogador
        self.alturaJogador = alturaJogador
    
    def jogo(self , janelaJogo):
        pygame.draw.rect(janelaJogo, self.cor, (self.x, self.y, self.larguraJogador, self.alturaJogador))

def jogo(janelaJogo, players):
    janelaJogo.fill(preto)

    for jogadores in players:
        jogadores.jogo(janela)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    jogadorUm = jogadores(10, altura/2 - alturaJogador/2, 20, 100)
    jogadorDois = jogadores(largura - 30, altura/2 - alturaJogador/2, 20, 100)
   

    while run:
        for event in pygame.event.get():
            clock.tick(60)
            jogo(janela, [jogadorUm, jogadorDois])
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()

if __name__ == '__main__':
    main()