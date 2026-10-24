"""
"""

import pygame # verifique o projeto.toml
import random
import numpy

class Mundo():
    def __init__(self, tamanho):
        self.tamanho = tamanho

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
        origem = mapa[int((self.tamanho-1)/2)][int((self.tamanho-1)/2)]
        return mapa

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

        return posicao_nova

    def renderizar_mapa(self, mapa, posicao = [0,0]):
        sala_numero = mapa[posicao[0]][posicao[1]]
        match sala_numero:
            case 0:
                salao_principal = pygame.image.load("salao_1.png")
            case 1:
                salao_principal = pygame.image.load("salao_2.png")
            case 2:
                salao_principal = pygame.image.load("salao_3.png")
            case 3:
                salao_principal = pygame.image.load("salao_1.png")

        return salao_principal



class Salas():
    def __init__(self):
        pass 

class Personagem():
    def __init__(self, velocidade):
        self.velocidade = velocidade

class Objeto():
    def __init__(self, quarto_x, quarto_y):
        self.x = quarto_x
        self.y = quarto_y

class ObjetoInteragível(Objeto):
    def __init__(self):
        pass 

class ObjetoEspecial(ObjetoInteragível):
    def __init__(self):
        pass 

mapa = Mundo(5)
