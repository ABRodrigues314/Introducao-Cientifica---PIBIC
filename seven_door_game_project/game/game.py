"""
"""

import pygame 
import random
from objetos import Mundo, Personagem, Objetos, Portoes

# ___________________________________________________________________________________________________
# Inicializando as classes
# Mundo

def _criar_mundo(tamanho):
    """
    """
    if tamanho <= 10:
        tamanho = 11
    elif tamanho % 2 == 0:
        tamanho += 1

    return Mundo(tamanho)

def _gerar_itens(dicionario):
    lista_itens = []
    for item in list(dicionario[0].keys()):
        lista_itens.append(Objetos(dicionario[1], dicionario[0][item][1], item))

    historico = [((dicionario[1]-1)/2,(dicionario[1]-1)/2)]    
    for item in lista_itens:
        historico = item.sortear_objetos(dicionario[0][item.nome][0], historico)

    return tuple(lista_itens)

def _blit_itens(lista_itens, mapa, tela, personagem, hit_box = False):
    for item in lista_itens:
        if item.mapa[mapa.posicao[0]][mapa.posicao[1]] == 1:
            item_= pygame.transform.scale(item.imagem, item.escala)
            tela.blit(item_, (mapa.LARGURA/2-item.escala[0]/2, mapa.ALTURA/2-item.escala[0]/2))
            if item.rect.colliderect(personagem.rect) and not item.contato:
                item.mapa[mapa.posicao[0]][mapa.posicao[1]] = 0
                # item.contato = True
            if hit_box:
                pygame.draw.rect(tela, (0,255,0), item.rect, 2)

def _ativa_hit_box(paredes, tela, personagem):
    quadrantes = ["Superior_esquerdo", "Superior_direito", "Inferior_esquerdo", "Inferior_direito"]

    for quadrante in quadrantes:
        for parede in paredes[mapa.salao_nome][quadrante]:
            pygame.draw.rect(tela, (255, 0, 0), parede, 2)

    pygame.draw.rect(tela, (0,255,0), personagem.rect, 2)

def contato_com_parede(paredes, mapa, personagem):
    contato = False
    velocidade_anterior = personagem.velocidade
    for parede in paredes[mapa.salao_nome][personagem.quadrante]:
        if personagem.rect.colliderect(parede):
            contato == True
            match personagem.direcao:
                case "N":
                    personagem.velocidade = 0.2
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("S")
                case "S":
                    personagem.velocidade = 0.2
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("N")
                case "R":
                    personagem.velocidade = 0.2
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("L")
                case "L":
                    personagem.velocidade = 0.2
                    while personagem.rect.colliderect(parede):
                        personagem.movimentacao("R")

            personagem.velocidade = velocidade_anterior

        contato = False

# Criando mapa
mapa = _criar_mundo(21)

# Criando personagem
personagem = Personagem(mapa.LARGURA/2 - 20, mapa.ALTURA/2 - 20)

# Criando itens
objetos = [{"chave" : [7,(40,40)],
           "bussola" : [12,(50,50)],
           "chapeu" : [12,(50,50)],
           "saco_de_moedas" : [20,(30,30)],
           "moeda" : [int(((mapa.tamanho**2)-1)/2), (20,20)]}, mapa.tamanho]
lista_itens = _gerar_itens(objetos)
chaves, bussola, chapeu_de_mago, saco_de_moedas, moedas = lista_itens[0], lista_itens[1], lista_itens[2], lista_itens[3], lista_itens[4]

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

    _blit_itens(lista_itens, mapa, tela, personagem, False)

    jogador = pygame.transform.scale(personagem.imagem, (50*personagem.tamanho, 50*personagem.tamanho))
    tela.blit(jogador, (personagem.posicao[0], personagem.posicao[1]))
    
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - personagem.ultimo_uptade > 200:
        personagem.estado = "parado"
        personagem.animacao(personagem.direcao, personagem.estado)

    contato_com_parede(paredes, mapa, personagem)
    # _______________________________________________________________________
    # mudança de salas (criar função)

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
    # Andar (criar função)

    if evento.type == pygame.KEYDOWN:
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
