import pygame
pygame.init()


largura, altura = 700, 500
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Pong, por Marco, Felipe e Matheus Rodrigues dos Santos')

fps = 60

branco = (255, 255, 255)
preto = (0, 0, 0)

larguraDoJogador, alturaDoJogador = 20, 100
raioDaBola = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10


class jogadores:
    cor = branco
    VEL = 4

    def __init__(self, x, y, largura, altura):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.largura = largura
        self.altura = altura

    def jogo(self, win):
        pygame.draw.rect(
            win, self.cor, (self.x, self.y, self.largura, self.altura))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class ball:
    MAX_VEL = 5
    cor = branco

    def __init__(self, x, y, raio):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.raio = raio
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def jogo(self, win):
        pygame.draw.circle(win, self.cor, (self.x, self.y), self.raio)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, jogador, ball, pontoDoJodadorUm, pontoDoJogadorDois):
    win.fill(preto)

    pontoDoJodadorUm_texto = SCORE_FONT.render(f"{pontoDoJodadorUm}", 1, branco)
    pontoDoJogadorDois_texto = SCORE_FONT.render(f"{pontoDoJogadorDois}", 1, branco)
    win.blit(pontoDoJodadorUm_texto, (largura//4 - pontoDoJodadorUm_texto.get_width()//2, 20))
    win.blit(pontoDoJogadorDois_texto, (largura * (3/4) -
                                pontoDoJogadorDois_texto.get_width()//2, 20))

    for jogadores in jogador:
        jogadores.jogo(win)


    ball.jogo(win)
    pygame.display.update()


def colisao(bola, jogadorUm, jogadorDois):
    if bola.y + bola.raio >= altura:
        bola.y_vel *= -1
    elif bola.y - bola.raio <= 0:
        bola.y_vel *= -1

    if bola.x_vel < 0:
        if bola.y >= jogadorUm.y and bola.y <= jogadorUm.y + jogadorUm.altura:
            if bola.x - bola.raio <= jogadorUm.x + jogadorUm.largura:
                bola.x_vel *= -1

                meio = jogadorUm.y + jogadorUm.altura / 2
                diferenca = meio - bola.y
                reduzirFatores = (jogadorUm.altura / 2) / bola.MAX_VEL
                y_vel = diferenca / reduzirFatores
                bola.y_vel = -1 * y_vel

    else:
        if bola.y >= jogadorDois.y and bola.y <= jogadorDois.y + jogadorDois.altura:
            if bola.x + bola.raio >= jogadorDois.x:
                bola.x_vel *= -1

                meio = jogadorDois.y + jogadorDois.altura / 2
                diferenca = meio - bola.y
                reduzirFatores = (jogadorDois.altura / 2) / bola.MAX_VEL
                y_vel = diferenca / reduzirFatores
                bola.y_vel = -1 * y_vel


def movimentoDoJogador(keys, jogadorUm, jogadorDois):
    if keys[pygame.K_w] and jogadorUm.y - jogadorUm.VEL >= 0:
        jogadorUm.move(up=True)
    if keys[pygame.K_s] and jogadorUm.y + jogadorUm.VEL + jogadorUm.altura <= altura:
        jogadorUm.move(up=False)

    if keys[pygame.K_UP] and jogadorDois.y - jogadorDois.VEL >= 0:
        jogadorDois.move(up=True)
    if keys[pygame.K_DOWN] and jogadorDois.y + jogadorDois.VEL + jogadorDois.altura <= altura:
        jogadorDois.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()

    jogadorUm = jogadores(10, altura//2 - alturaDoJogador //
                         2, larguraDoJogador, alturaDoJogador)
    jogadorDois = jogadores(largura - 10 - larguraDoJogador, altura //
                          2 - alturaDoJogador//2, larguraDoJogador, alturaDoJogador)
    bola = ball(largura // 2, altura // 2, raioDaBola)

    pontoDoJodadorUm = 0
    pontoDoJogadorDois = 0

    while run:
        clock.tick(fps)
        draw(janela, [jogadorUm, jogadorDois], bola, pontoDoJodadorUm, pontoDoJogadorDois)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        movimentoDoJogador(keys, jogadorUm, jogadorDois)

        bola.move()
        colisao(bola, jogadorUm, jogadorDois)

        if bola.x < 0:
            pontoDoJogadorDois += 1
            bola.reset()
        elif bola.x > largura:
            pontoDoJodadorUm += 1
            bola.reset()

        vitoria = False
        if pontoDoJodadorUm >= WINNING_SCORE:
            vitoria = True
            textoDeVitoria = "O jogador um ganhou!"
        elif pontoDoJogadorDois >= WINNING_SCORE:
            vitoria = True
            textoDeVitoria = "O jogador dois ganhou!"

        if vitoria:
            texto = SCORE_FONT.render(textoDeVitoria, 1, branco)
            janela.blit(texto, (largura//2 - texto.get_largura() //
                            2, altura//2 - texto.altura()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            bola.reset()
            jogadorUm.reset()
            jogadorDois.reset()
            pontoDoJodadorUm = 0
            pontoDoJogadorDois = 0

    pygame.quit()


if __name__ == '__main__':
    main()