"""
"""

import pygame # verifique o projeto.toml
import random

class Mundo():
    def __init__(self):
        pass 

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