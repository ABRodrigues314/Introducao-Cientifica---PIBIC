"""
"""

import pygame # verifique o projeto.toml
import random
import numpy
import time

# ___________________________________________________________________________________________________
# Definindo as classes

class Mundo():
    """"""
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.LARGURA = 1000
        self.ALTURA = 800
        mapa, origem = self.gerar_mapa()
        self.mapa = mapa
        self.posicao = [0,0]
        self.salao = pygame.image.load("Salao/salao_1.png")

    def gerar_mapa(self):
        mapa = []
        while len(mapa) != self.tamanho:
            fileira = []
            while len(fileira) != self.tamanho:
                numero_aleatorio = random.randint(0,3)
                if fileira == [] or numero_aleatorio != fileira[-1]:
                    fileira.append(numero_aleatorio)
            mapa.append(fileira[:])

        mapa[int((self.tamanho-1)/2)][int((self.tamanho-1)/2)] = 0
        origem = [[int((self.tamanho-1)/2)],[int((self.tamanho-1)/2)]]
        return mapa, origem

    def mover_mapa(self, posicao, sentido):
        posicao_nova = []
        match sentido:
            case "N":
                posicao_nova = [posicao[0],posicao[1]+1]
            case "S":
                posicao_nova = [posicao[0],posicao[1]-1]
            case "L":
                posicao_nova = [posicao[0]+1,posicao[1]]
            case "O":
                posicao_nova = [posicao[0]-1,posicao[1]]
            case _:
                posisao_nova = posicao

        self.posicao = posicao_nova

    def renderizar_mapa(self, mapa, posicao = [0,0]):
        # Criar um tratamento do erro index out of range
        
        sala_numero = mapa[posicao[0]][posicao[1]]
        match sala_numero:
            case 0:
                salao_principal = pygame.image.load("Salao/salao_1.png")
            case 1:
                salao_principal = pygame.image.load("Salao/salao_2.png")
            case 2:
                salao_principal = pygame.image.load("Salao/salao_3.png")
            case 3:
                salao_principal = pygame.image.load("Salao/salao_4.png")

        self.salao = salao_principal


class Personagem():
    """"""
    def __init__(self, posicao_x, posicao_y, velocidade=1):
        self.velocidade = velocidade
        self.posicao = [posicao_x, posicao_y]
        self.imagem = pygame.image.load("Personagem/personagem_frente_3.png")

    def animacao(self, direcao): # Aqui tá com problema
        """
        É preciso verificar o jeito certo de comparar imagens, pois:
        pygame.image.load(Imagem) == <Surface(130x140x32, global_alpha=255)> -> True
        para toda imagem.
        """
        
        match direcao:
            case "N":
                imagem1 = pygame.image.load("Personagem/personagem_costas_1.png")
                imagem2 = pygame.image.load("Personagem/personagem_costas_3.png")
                imagem3 = pygame.image.load("Personagem/personagem_costas_2.png")

                if self.imagem == imagem1:
                    self.imagem = imagem2
                if self.imagem == imagem2:
                    self.imagem = imagem3
                if self.imagem == imagem3:
                    self.imagem = imagem1
                print(self.imagem)

            case "S":
                imagem1 = pygame.image.load("Personagem/personagem_frente_1.png")
                imagem2 = pygame.image.load("Personagem/personagem_frente_3.png")
                imagem3 = pygame.image.load("Personagem/personagem_frente_2.png")

                if self.imagem == imagem1:
                    self.imagem = imagem2
                if self.imagem == imagem2:
                    self.imagem = imagem3
                if self.imagem == imagem3:
                    self.imagem = imagem1
                print(self.imagem)

            case "R":
                imagem1 = pygame.image.load("Personagem/personagem_direita_1.png")
                imagem2 = pygame.image.load("Personagem/personagem_direita_3.png")
                imagem3 = pygame.image.load("Personagem/personagem_direita_2.png")

                if self.imagem == imagem1:
                    self.imagem = imagem2
                if self.imagem == imagem2:
                    self.imagem = imagem3
                if self.imagem == imagem3:
                    self.imagem = imagem1
                print(self.imagem)

            case "L":
                imagem1 = pygame.image.load("Personagem/personagem_esquerda_1.png")
                imagem2 = pygame.image.load("Personagem/personagem_esquerda_3.png")
                imagem3 = pygame.image.load("Personagem/personagem_esquerda_2.png")

                if self.imagem == imagem1:
                    self.imagem = imagem2
                if self.imagem == imagem2:
                    self.imagem = imagem3
                if self.imagem == imagem3:
                    self.imagem = imagem1
                print(self.imagem)
            case _:
                print("Uai")


    def movimentacao(self, direcao):
        posicao_x = self.posicao[0]
        posicao_y = self.posicao[1]

        match direcao:
            case "N":
                posicao_y -= 5*self.velocidade
                self.animacao(direcao)
            case "S":
                posicao_y += 5*self.velocidade
                self.animacao(direcao)
            case "R":
                posicao_x += 5*self.velocidade
                self.animacao(direcao)
            case "L":
                posicao_x -= 5*self.velocidade
                self.animacao(direcao)

        self.posicao = [posicao_x, posicao_y]


    def contato_parede(self):
        pass

class Salas():
    """"""
    def __init__(self):
        pass 

class Objeto():
    """"""
    def __init__(self, quarto_x, quarto_y):
        self.x = quarto_x
        self.y = quarto_y

class ObjetoInteragível(Objeto):

    """"""
    def __init__(self):
        pass 

class ObjetoEspecial(ObjetoInteragível):
    """"""
    def __init__(self):
        pass 

# ___________________________________________________________________________________________________
# Inicializando as classes
mapa = Mundo(5)
personagem = Personagem(mapa.LARGURA/2, mapa.ALTURA/2)
print(mapa.mapa)

# ___________________________________________________________________________________________________
# Inicializando o jogo
pygame.init()

tela = pygame.display.set_mode((mapa.LARGURA, mapa.ALTURA))
pygame.display.set_caption("Seven Door")
relogio = pygame.time.Clock()

rodando = True
while rodando:

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

    salao = pygame.transform.scale(mapa.salao, (mapa.LARGURA, mapa.ALTURA))
    tela.blit(salao)

    jogador = pygame.transform.scale(personagem.imagem, (50, 50))
    tela.blit(jogador, (personagem.posicao[0], personagem.posicao[1]))

    if evento.type == pygame.KEYDOWN:
        # if evento.key == pygame.K_UP:
        #     mapa.mover_mapa(mapa.posicao, "N")
        #     mapa.renderizar_mapa(mapa.mapa, mapa.posicao)
        #     print("Norte")
        #     time.sleep(0.3)

        # if evento.key == pygame.K_DOWN:
        #     mapa.mover_mapa(mapa.posicao, "S")
        #     mapa.renderizar_mapa(mapa.mapa, mapa.posicao)
        #     print("Sul")
        #     time.sleep(0.3)
            
        # if evento.key == pygame.K_LEFT:
        #     mapa.mover_mapa(mapa.posicao, "O")
        #     mapa.renderizar_mapa(mapa.mapa, mapa.posicao)
        #     print("Oeste")
        #     time.sleep(0.3)

        # if evento.key == pygame.K_RIGHT:
        #     mapa.mover_mapa(mapa.posicao, "L")
        #     mapa.renderizar_mapa(mapa.mapa, mapa.posicao)
        #     print("Leste")
        #     time.sleep(0.3)

        if evento.key == pygame.K_UP:
            personagem.movimentacao("N")
        if evento.key == pygame.K_DOWN:
            personagem.movimentacao("S")
        if evento.key == pygame.K_LEFT:
            personagem.movimentacao("L")
        if evento.key == pygame.K_RIGHT:
            personagem.movimentacao("R")



    pygame.display.flip()
    relogio.tick(60)
    

pygame.quit()

