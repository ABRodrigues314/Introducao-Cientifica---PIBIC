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
        self.posicao = [int((tamanho-1)/2),int((tamanho-1)/2)]
        self.saloes = {"salao_1" : [pygame.image.load("Salao/salao_1.png")],
                       "salao_2" : [pygame.image.load("Salao/salao_2.png")],
                       "salao_3" : [pygame.image.load("Salao/salao_3.png")],
                       "salao_4" : [pygame.image.load("Salao/salao_4.png")]}
        self.salao_nome = "salao_1"
        self.salao = self.saloes[self.salao_nome][0]

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
            case "R":
                posicao_nova = [posicao[0]-1,posicao[1]]
            case _:
                posisao_nova = posicao

        self.posicao = posicao_nova

    def renderizar_mapa(self):
        # Criar um tratamento do erro index out of range
        
        mapa = self.mapa
        posicao_mapa = self.posicao
        print(posicao_mapa)
        sala_numero = mapa[posicao_mapa[0]][posicao_mapa[1]]
        match sala_numero:
            case 0:
                salao_principal = self.saloes["salao_1"][0]
                self.salao_nome = "salao_1"
            case 1:
                salao_principal = self.saloes["salao_2"][0]
                self.salao_nome = "salao_2"
            case 2:
                salao_principal = self.saloes["salao_3"][0]
                self.salao_nome = "salao_3"
            case 3:
                salao_principal = self.saloes["salao_4"][0]
                self.salao_nome = "salao_4"

        self.salao = salao_principal

    def definir_paredes(self):
        paredes = {"salao_1" : {"Superior_esquerdo" : [
                        pygame.Rect(0, 0, 402, 110),
                        pygame.Rect(0, 0, 200, 155),
                        pygame.Rect(0, 0, 100, 360),
                        ],
                        "Superior_direito" : [
                        pygame.Rect(598, 0, 1000, 110),
                        pygame.Rect(800, 0, 1000, 155),
                        pygame.Rect(900, 0, 1000, 360),
                        ],
                        "Inferior_esquerdo" : [
                        pygame.Rect(0, 655, 402, 150),
                        pygame.Rect(0, 615, 200, 170),
                        pygame.Rect(0, 440, 100, 360),
                        ],
                        "Inferior_direito" : [
                        pygame.Rect(595, 655, 402, 150),
                        pygame.Rect(800, 615, 200, 170),
                        pygame.Rect(900, 440, 100, 360),
                        ]},

            "salao_2" : {"Superior_esquerdo" : [
                        pygame.Rect(0, 0, 430, 160),
                        pygame.Rect(0, 0, 265, 240),
                        pygame.Rect(0, 0, 200, 315),
                        ],
                        "Superior_direito" : [
                        pygame.Rect(570, 0, 1000, 160),
                        pygame.Rect(735, 0, 1000, 240),
                        pygame.Rect(800, 0, 1000, 315),
                        ],
                        "Inferior_esquerdo" : [
                        pygame.Rect(0, 560, 430, 300),
                        pygame.Rect(0, 530, 265, 240),
                        pygame.Rect(0, 430, 200, 320),
                        ],
                        "Inferior_direito" : [
                        pygame.Rect(570, 560, 430, 300),
                        pygame.Rect(735, 530, 265, 240),
                        pygame.Rect(800, 430, 200, 320),
                        ]},
            "salao_3" : {"Superior_esquerdo" : [
                        pygame.Rect(0, 0, 445, 160),
                        pygame.Rect(0, 0, 280, 240),
                        pygame.Rect(0, 0, 215, 360),
                        ],
                        "Superior_direito" : [
                        pygame.Rect(555, 0, 1000, 160),
                        pygame.Rect(720, 0, 1000, 240),
                        pygame.Rect(785, 0, 1000, 360),
                        ],
                        "Inferior_esquerdo" : [
                        pygame.Rect(0, 583, 445, 300),
                        pygame.Rect(0, 545, 280, 240),
                        pygame.Rect(0, 435, 215, 320),
                        ],
                        "Inferior_direito" : [
                        pygame.Rect(555, 583, 430, 300),
                        pygame.Rect(720, 545, 265, 240),
                        pygame.Rect(785, 435, 220, 320),
                        ]},
            "salao_4" : {"Superior_esquerdo" : [
                        pygame.Rect(0, 0, 415, 100),
                        pygame.Rect(0, 0, 230, 145),
                        pygame.Rect(0, 0, 110, 345),
                        ],
                        "Superior_direito" : [
                        pygame.Rect(585, 0, 1000, 100),
                        pygame.Rect(770, 0, 1000, 145),
                        pygame.Rect(890, 0, 1000, 345),
                        ],
                        "Inferior_esquerdo" : [
                        pygame.Rect(0, 650, 415, 200),
                        pygame.Rect(0, 600, 230, 170),
                        pygame.Rect(0, 440, 110, 360),
                        ],
                        "Inferior_direito" : [
                        pygame.Rect(582, 650, 415, 200),
                        pygame.Rect(772, 602, 230, 170),
                        pygame.Rect(890, 440, 110, 360),
                        ]}}

        return paredes

class Personagem():
    """"""
    def __init__(self, posicao_x, posicao_y, velocidade=1):
        self.velocidade = velocidade
        self.posicao = [posicao_x, posicao_y]
        self.tamanho = 1
        self.quadro = 1
        self.estado = "parado"
        self.direcao = "S"
        self.rect = pygame.Rect(self.posicao[0]+6, self.posicao[1]-1, 40, 48)
        self.intervalo_animacao = 150
        self.ultimo_uptade = pygame.time.get_ticks()
        self.animacoes = {"andando" : {"N" : [pygame.image.load("Personagem/personagem_costas_2.png"),
                                 pygame.image.load("Personagem/personagem_costas_1.png")],
                        "S" : [pygame.image.load("Personagem/personagem_frente_2.png"),
                               pygame.image.load("Personagem/personagem_frente_1.png")],
                        "R" : [pygame.image.load("Personagem/personagem_direita_2.png"),
                               pygame.image.load("Personagem/personagem_direita_1.png")],
                        "L" : [pygame.image.load("Personagem/personagem_esquerda_2.png"),
                               pygame.image.load("Personagem/personagem_esquerda_1.png")]},
                        "parado" : {"N" : pygame.image.load("Personagem/personagem_costas_3.png"),
                        "S" : pygame.image.load("Personagem/personagem_frente_3.png"),
                        "R" : pygame.image.load("Personagem/personagem_direita_3.png"),
                        "L" : pygame.image.load("Personagem/personagem_esquerda_3.png")}}
        self.imagem = self.animacoes[self.estado][self.direcao]
        self.quadrante = "Superior_esquerdo"

    def animacao(self, direcao, estado):
        """
        É preciso verificar o jeito certo de comparar imagens, pois:
        pygame.image.load(Imagem) == <Surface(130x140x32, global_alpha=255)> -> True
        para toda imagem.
        """

        tempo_atual = pygame.time.get_ticks()
        self.direcao = direcao
        if tempo_atual - self.ultimo_uptade > self.intervalo_animacao:
            if estado == "andando":
                match direcao:
                    case "N":

                        if self.quadro == 1:
                            self.imagem = self.animacoes[estado][direcao][0]
                            self.quadro = 2

                        elif self.quadro == 2:
                            self.imagem = self.animacoes[estado][direcao][1]
                            self.quadro = 1

                    case "S":

                        if self.quadro == 1:
                            self.imagem = self.animacoes[estado][direcao][0]
                            self.quadro = 2

                        elif self.quadro == 2:
                            self.imagem = self.animacoes[estado][direcao][1]
                            self.quadro = 1

                    case "R":
                        if self.quadro == 1:
                            self.imagem = self.animacoes[estado][direcao][0]
                            self.quadro = 2

                        elif self.quadro == 2:
                            self.imagem = self.animacoes[estado][direcao][1]
                            self.quadro = 1

                    case "L":
                        if self.quadro == 1:
                            self.imagem = self.animacoes[estado][direcao][0]
                            self.quadro = 2

                        elif self.quadro == 2:
                            self.imagem = self.animacoes[estado][direcao][1]
                            self.quadro = 1

                    case _:
                        print("Uai(andando)")

            elif estado == "parado":
                match direcao:
                    case "N":
                        self.imagem = self.animacoes[estado][direcao]

                    case "S":
                        self.imagem = self.animacoes[estado][direcao]

                    case "R":
                        self.imagem = self.animacoes[estado][direcao]

                    case "L":
                        self.imagem = self.animacoes[estado][direcao]

                    case _:
                        print("Uai(parado)")

            else:
                print("Uai(else)")

            self.ultimo_uptade = pygame.time.get_ticks()

    def movimentacao(self, direcao):
        posicao_x = self.posicao[0]
        posicao_y = self.posicao[1]

        match direcao:
            case "N":
                posicao_y -= 10*self.velocidade
            case "S":
                posicao_y += 10*self.velocidade
            case "R":
                posicao_x += 10*self.velocidade
            case "L":
                posicao_x -= 10*self.velocidade
        
        self.posicao = [posicao_x, posicao_y]
        self.rect = pygame.Rect(self.posicao[0]+6, self.posicao[1]-1, 40, 48)

    def localizar_quadrante(self, dimensoes_mundo: list):
        if self.posicao[0] > dimensoes_mundo[0]/2:
            if self.posicao[1] > dimensoes_mundo[1]/2:
                self.quadrante = "Inferior_direito"
            elif self.posicao[1] < dimensoes_mundo[1]/2:
                self.quadrante = "Superior_direito"
        elif self.posicao[0] < dimensoes_mundo[0]/2:
            if self.posicao[1] > dimensoes_mundo[1]/2:
                self.quadrante = "Inferior_esquerdo"
            elif self.posicao[1] < dimensoes_mundo[1]/2:
                self.quadrante = "Superior_esquerdo"

class Objetos():
    """"""
    def __init__(self, tamanho, imagem):
        self.tamanho = tamanho
        self.mapa = self.gerar_mapa()
        self.imagens = {"chave" : pygame.image.load("Itens/chave_portao.png"),
                        "bussola" : pygame.image.load("Itens/bussola.png"),
                        "chapeu" : pygame.image.load("Itens/chapeu_de_mago.png"),
                        "saco_de_moedas" : pygame.image.load("Itens/saco_de_moedas.png"),
                        "moeda" : pygame.image.load("Itens/moedas.png")}
        self.imagem = self.imagens[imagem]
        self.rects = {"chave" : (480, 380, 40, 40),
                    "bussola" : (475, 375, 50, 50),
                    "chapeu" : (475, 375, 50, 50),
                    "saco_de_moedas" : (485, 385, 30, 30),
                    "moeda" : (490, 390, 20, 20)}

        self.rect = pygame.Rect(self.rects[imagem][0], 
                                self.rects[imagem][1], 
                                self.rects[imagem][2], 
                                self.rects[imagem][3])

    def gerar_mapa(self):
        mapa = []
        while len(mapa) != self.tamanho:
            fileira = []
            while len(fileira) != self.tamanho:
                fileira.append(0)
            mapa.append(fileira[:])
        
        return mapa

    def sortear_objetos(self, quantidade: int, historico):

        while quantidade != 0:
            x = random.randint(0, self.tamanho-1)
            y = random.randint(0, self.tamanho-1)
            if (x,y) not in historico:
                self.mapa[x][y] = 1
                historico.append((x,y))
                quantidade -= 1

        return historico

class Portoes():
    """"""
    def __init__(self):
        pass 

# ___________________________________________________________________________________________________
# Inicializando as classes
# Mundo
n = 21
if n % 2 == 1 and n > 10:
    mapa = Mundo(n)
else:
    print("Opa, valor inválido")

# personagem
personagem = Personagem(mapa.LARGURA/2 - 20, mapa.ALTURA/2 - 20, velocidade=1)

# Objetos
chaves = Objetos(mapa.tamanho, "chave")
bussola = Objetos(mapa.tamanho, "bussola")
chapeu_de_mago = Objetos(mapa.tamanho, "chapeu")
saco_de_moedas = Objetos(mapa.tamanho, "saco_de_moedas")
moedas = Objetos(mapa.tamanho, "moeda")

historico = chaves.sortear_objetos(7, [((mapa.tamanho-1)/2,(mapa.tamanho-1)/2)])
historico = bussola.sortear_objetos(12, historico)
historico = chapeu_de_mago.sortear_objetos(12, historico)
historico = saco_de_moedas.sortear_objetos(20, historico)
moedas.sortear_objetos(int(((mapa.tamanho**2)-1)/2), historico)

# ___________________________________________________________________________________________________
# Inicializando o jogo
pygame.init()

tela = pygame.display.set_mode((mapa.LARGURA, mapa.ALTURA))
pygame.display.set_caption("Seven Door")
relogio = pygame.time.Clock()
paredes = mapa.definir_paredes()

rodando = True
while rodando:

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

    salao = pygame.transform.scale(mapa.salao, (mapa.LARGURA, mapa.ALTURA))
    tela.blit(salao)

    if chaves.mapa[mapa.posicao[0]][mapa.posicao[1]] == 1:
        chave_ = pygame.transform.scale(chaves.imagem, (40,40))
        tela.blit(chave_, (mapa.LARGURA/2-20, mapa.ALTURA/2-20))
        if chaves.rect.colliderect(personagem.rect):
            chaves.mapa[mapa.posicao[0]][mapa.posicao[1]] = 0
        pygame.draw.rect(tela, (0,255,0), chaves.rect, 2)
    
    if bussola.mapa[mapa.posicao[0]][mapa.posicao[1]] == 1:
        bussola_ = pygame.transform.scale(bussola.imagem, (50,50))
        tela.blit(bussola_, (mapa.LARGURA/2-25, mapa.ALTURA/2-25))
        if bussola.rect.colliderect(personagem.rect):
            bussola.mapa[mapa.posicao[0]][mapa.posicao[1]] = 0
        pygame.draw.rect(tela, (0,255,0), bussola.rect, 2)
    
    if chapeu_de_mago.mapa[mapa.posicao[0]][mapa.posicao[1]] == 1:
        chapeu_de_mago_ = pygame.transform.scale(chapeu_de_mago.imagem, (50,50))
        tela.blit(chapeu_de_mago_, (mapa.LARGURA/2-25, mapa.ALTURA/2-25))
        if chapeu_de_mago.rect.colliderect(personagem.rect):
            chapeu_de_mago.mapa[mapa.posicao[0]][mapa.posicao[1]] = 0
        pygame.draw.rect(tela, (0,255,0), chapeu_de_mago.rect, 2)
    
    if saco_de_moedas.mapa[mapa.posicao[0]][mapa.posicao[1]] == 1:
        saco_de_moedas_ = pygame.transform.scale(saco_de_moedas.imagem, (30,30))
        tela.blit(saco_de_moedas_, (mapa.LARGURA/2-15, mapa.ALTURA/2-15))
        if saco_de_moedas.rect.colliderect(personagem.rect):
            saco_de_moedas.mapa[mapa.posicao[0]][mapa.posicao[1]] = 0
        pygame.draw.rect(tela, (0,255,0), saco_de_moedas.rect, 2)
    
    if moedas.mapa[mapa.posicao[0]][mapa.posicao[1]] == 1:
        moedas_ = pygame.transform.scale(moedas.imagem, (20,20))
        tela.blit(moedas_, (mapa.LARGURA/2-10, mapa.ALTURA/2-10))
        if moedas.rect.colliderect(personagem.rect):
            moedas.mapa[mapa.posicao[0]][mapa.posicao[1]] = 0
        pygame.draw.rect(tela, (0,255,0), moedas.rect, 2)

    jogador = pygame.transform.scale(personagem.imagem, (50*personagem.tamanho, 50*personagem.tamanho))
    tela.blit(jogador, (personagem.posicao[0], personagem.posicao[1]))
    
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - personagem.ultimo_uptade > 200:
        personagem.estado = "parado"
        personagem.animacao(personagem.direcao, personagem.estado)

    # _______________________________________________________________________
    
    for parede in paredes[mapa.salao_nome]["Superior_esquerdo"]:
        pygame.draw.rect(tela, (255, 0, 0), parede, 2)

    for parede in paredes[mapa.salao_nome]["Superior_direito"]:
        pygame.draw.rect(tela, (255, 0, 0), parede, 2)

    for parede in paredes[mapa.salao_nome]["Inferior_esquerdo"]:
        pygame.draw.rect(tela, (255, 0, 0), parede, 2)

    for parede in paredes[mapa.salao_nome]["Inferior_direito"]:
        pygame.draw.rect(tela, (255, 0, 0), parede, 2)

    pygame.draw.rect(tela, (0,255,0), personagem.rect, 2)

    # _______________________________________________________________________
    # Contato com a parede
    contato = False
    for parede in paredes[mapa.salao_nome][personagem.quadrante]:
        if personagem.rect.colliderect(parede):
            contato == True
            match personagem.direcao:
                case "N":
                    personagem.velocidade = 0.1
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("S")
                case "S":
                    personagem.velocidade = 0.1
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("N")
                case "R":
                    personagem.velocidade = 0.1
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("L")
                case "L":
                    personagem.velocidade = 0.1
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("R")

            personagem.velocidade = 1

        contato = False

    # _______________________________________________________________________
    # mudança de salas

    if personagem.posicao[0] < -25 or personagem.posicao[0] > 975 or personagem.posicao[1] < -25 or personagem.posicao[1] > 775:
        mapa.mover_mapa(mapa.posicao, personagem.direcao)
        mapa.renderizar_mapa()
        match personagem.direcao:
            case "N":
                personagem.posicao = [mapa.LARGURA/2, 770]
            case "S":
                personagem.posicao = [mapa.LARGURA/2, -20]
            case "R":
                personagem.posicao = [-20, (mapa.ALTURA/2)-30]
            case "L":
                personagem.posicao = [970, (mapa.ALTURA/2)-30]

    # _______________________________________________________________________
    # Andar

    if evento.type == pygame.KEYDOWN and not contato:
        personagem.estado = "andando"
        if evento.key == pygame.K_UP:
            personagem.movimentacao("N")
            personagem.animacao("N",personagem.estado)
        if evento.key == pygame.K_DOWN:
            personagem.movimentacao("S")
            personagem.animacao("S",personagem.estado)
        if evento.key == pygame.K_LEFT:
            personagem.movimentacao("L")
            personagem.animacao("L",personagem.estado)
        if evento.key == pygame.K_RIGHT:
            personagem.movimentacao("R")
            personagem.animacao("R",personagem.estado)
    personagem.localizar_quadrante([mapa.LARGURA, mapa.ALTURA])
        
    pygame.display.flip()
    relogio.tick(60)
    
pygame.quit()
