import math
import random

import pygame

LARGURA, ALTURA = 960, 720
FPS = 60
MAX_PERDAS = 3
BONUS_DIA = 25

COR_FUNDO = (245, 235, 220)
COR_HUD = (48, 40, 36)
COR_TEXTO = (45, 35, 30)
COR_SLOT = (255, 252, 245)
COR_SLOT_VAZIO = (236, 228, 214)
COR_BORDA = (90, 70, 60)
COR_BANCADA = (154, 104, 64)
COR_BANCADA_ESC = (122, 80, 48)
COR_VERDE = (66, 168, 88)
COR_VERDE_ESC = (50, 130, 68)
COR_AMARELO = (238, 188, 60)
COR_VERMELHO = (214, 72, 62)
COR_BOTAO = (252, 246, 234)
COR_BOTAO_HOVER = (240, 228, 206)

INGREDIENTES = {
    "pao": ("Pão", (226, 174, 96)),
    "carne": ("Carne", (126, 74, 44)),
    "queijo": ("Queijo", (255, 202, 64)),
    "alface": ("Alface", (110, 190, 82)),
    "tomate": ("Tomate", (220, 72, 62)),
    "ovo": ("Ovo", (250, 246, 230)),
}
ORDEM_BOTOES = ["pao", "carne", "queijo", "alface", "tomate", "ovo"]

RECEITAS = [
    ("X-Burger", ["pao", "carne"]),
    ("X-Especial", ["pao", "carne", "queijo"]),
    ("X-Salada", ["pao", "carne", "queijo", "alface"]),
    ("X-Leve", ["pao", "carne", "alface", "tomate"]),
    ("X-Tomate", ["pao", "carne", "queijo", "tomate"]),
    ("Vegetariano", ["pao", "ovo", "alface", "tomate"]),
    ("X-Chefe", ["pao", "carne", "queijo", "alface", "tomate"]),
    ("Morning", ["pao", "ovo", "queijo", "alface"]),
]

NOMES = [
    "Ana", "Bruno", "Carla", "Diego", "Eva", "Felipe", "Gabriela", "Hugo",
    "Iris", "Joao", "Karla", "Lucas", "Marta", "Nina", "Otavio", "Paula",
]

PELES = [
    (255, 220, 190), (240, 196, 156), (225, 175, 130),
    (190, 140, 100), (150, 105, 75), (110, 78, 56),
]
CABELOS = [
    (40, 30, 25), (90, 55, 30), (180, 140, 70), (60, 60, 60),
    (160, 50, 40), (30, 30, 30), (210, 200, 185),
]

RET_SLOTS = [pygame.Rect(20, 66, 450, 350), pygame.Rect(490, 66, 450, 350)]
RET_BANCADA = pygame.Rect(0, 430, LARGURA, ALTURA - 430)
RET_SERVIR = pygame.Rect(450, 615, 300, 75)
RET_LIMPAR = pygame.Rect(760, 615, 180, 75)


def criar_botoes():
    botoes = []
    x0, y0, w, h, gap = 450, 440, 150, 70, 20
    for i, chave in enumerate(ORDEM_BOTOES):
        col, linha = i % 3, i // 3
        r = pygame.Rect(x0 + col * (w + gap), y0 + linha * (h + gap), w, h)
        botoes.append((chave, r))
    return botoes


BOTOES = criar_botoes()


class Cliente:
    def __init__(self, paciencia_max):
        nome_prato, ingredientes = random.choice(RECEITAS)
        self.nome_prato = nome_prato
        self.pedido = list(ingredientes)
        self.paciencia_max = paciencia_max
        self.paciencia = paciencia_max
        self.nome = random.choice(NOMES)
        self.cor_pele = random.choice(PELES)
        self.cor_cabelo = random.choice(CABELOS)


class Jogo:
    def __init__(self):
        pygame.font.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Lanches do Chefe")
        self.relogio = pygame.time.Clock()
        self._fontes = {}
        self.msg = None
        self.msg_t = 0.0
        self.bonus = 0
        self.clientes = [None, None]
        self.prato = []
        self.estado = "titulo"
        self.dia = 1
        self.dinheiro = 0
        self.meta = 0
        self.perdas = 0
        self.atendidos = 0
        self.pendentes = 0
        self.paciencia_max = 22.0
        self.timer_spawn = 0.0

    # ---------- fontes / texto ----------

    def f(self, tam, negrito=False):
        chave = (tam, negrito)
        if chave not in self._fontes:
            self._fontes[chave] = pygame.font.SysFont("arial", tam, bold=negrito)
        return self._fontes[chave]

    def texto(self, s, tam, cor, pos, centro=False, negrito=False):
        img = self.f(tam, negrito).render(s, True, cor)
        ret = img.get_rect(center=pos) if centro else img.get_rect(topleft=pos)
        self.tela.blit(img, ret)
        return ret

    def mensagem(self, s, cor):
        self.msg = (s, cor)
        self.msg_t = 2.5

    # ---------- lógica ----------

    def iniciar_dia(self):
        self.meta = 4 + self.dia
        self.atendidos = 0
        self.pendentes = self.meta
        self.perdas = 0
        self.paciencia_max = max(8.0, 22.0 - (self.dia - 1) * 2.0)
        self.clientes = [None, None]
        self.prato = []
        self.timer_spawn = 0.0
        self.msg = None
        self.msg_t = 0.0

    def reiniciar_jogo(self):
        self.dia = 1
        self.dinheiro = 0
        self.bonus = 0
        self.clientes = [None, None]
        self.prato = []
        self.estado = "titulo"

    def esperados(self):
        if self.prato and any(c and c.pedido == self.prato for c in self.clientes):
            return set()
        esperado = set()
        n = len(self.prato)
        for cli in self.clientes:
            if cli and len(cli.pedido) > n and cli.pedido[:n] == self.prato:
                esperado.add(cli.pedido[n])
        return esperado

    def clicar_ingrediente(self, chave):
        if not any(self.clientes):
            self.mensagem("Nenhum pedido ativo no momento.", COR_VERMELHO)
            return
        if self.prato and any(c and c.pedido == self.prato for c in self.clientes):
            self.mensagem("Prato pronto! Clique em SERVIR.", COR_VERDE)
            return
        if chave in self.esperados():
            self.prato.append(chave)
        else:
            self.prato = []
            nome = INGREDIENTES[chave][0]
            self.mensagem(f"Errou! {nome} nao e o proximo. Prato zerado.", COR_VERMELHO)

    def limpar(self):
        if self.prato:
            self.prato = []
            self.mensagem("Prato limpo.", COR_AMARELO)

    def servir(self):
        if not self.prato:
            self.mensagem("O prato esta vazio!", COR_VERMELHO)
            return
        for i, cli in enumerate(self.clientes):
            if cli and cli.pedido == self.prato:
                frac = cli.paciencia / cli.paciencia_max
                bonus = round(15 * frac)
                ganho = 10 + bonus
                self.dinheiro += ganho
                self.atendidos += 1
                extra = f" (+${bonus} de bonus)" if bonus else ""
                self.mensagem(
                    f"+${ganho}{extra} - {cli.nome} aprovou o {cli.nome_prato}!",
                    COR_VERDE,
                )
                self.clientes[i] = None
                self.prato = []
                return
        self.prato = []
        self.mensagem("Esse prato nao e o pedido de ninguem!", COR_VERMELHO)

    def atualizar(self, dt):
        if self.msg_t > 0:
            self.msg_t -= dt
        if self.timer_spawn > 0:
            self.timer_spawn -= dt

        for i, cli in enumerate(self.clientes):
            if cli is None:
                continue
            cli.paciencia -= dt
            if cli.paciencia <= 0:
                self.clientes[i] = None
                self.perdas += 1
                self.prato = []
                self.mensagem(
                    f"{cli.nome} nao aguentou e foi embora! "
                    f"Perdas: {self.perdas}/{MAX_PERDAS}",
                    COR_VERMELHO,
                )

        if self.perdas >= MAX_PERDAS:
            self.estado = "fim"
            return

        if self.timer_spawn <= 0 and self.pendentes > 0:
            for i, cli in enumerate(self.clientes):
                if cli is None:
                    self.clientes[i] = Cliente(self.paciencia_max)
                    self.pendentes -= 1
                    self.timer_spawn = 1.5
                    break

        if self.pendentes == 0 and all(c is None for c in self.clientes):
            self.bonus = BONUS_DIA * self.dia
            self.dinheiro += self.bonus
            self.estado = "dia_completo"

    def clique(self, pos):
        if self.estado == "titulo":
            self.iniciar_dia()
            self.estado = "jogando"
            return
        if self.estado == "dia_completo":
            self.dia += 1
            self.iniciar_dia()
            self.estado = "jogando"
            return
        if self.estado == "fim":
            self.reiniciar_jogo()
            return
        for chave, ret in BOTOES:
            if ret.collidepoint(pos):
                self.clicar_ingrediente(chave)
                return
        if RET_SERVIR.collidepoint(pos):
            self.servir()
        elif RET_LIMPAR.collidepoint(pos):
            self.limpar()

    # ---------- desenho ----------

    def desenhar_icone(self, chave, x, y, tam, indice=None):
        nome, cor = INGREDIENTES[chave]
        r = pygame.Rect(x, y, tam, tam)
        pygame.draw.rect(self.tela, cor, r, border_radius=6)
        pygame.draw.rect(self.tela, COR_BORDA, r, 2, border_radius=6)
        lab = self.f(11).render(nome, True, COR_TEXTO)
        self.tela.blit(lab, lab.get_rect(center=(x + tam // 2, y + tam + 9)))
        if indice is not None:
            n = self.f(11, True).render(str(indice + 1), True, (70, 60, 50))
            self.tela.blit(n, (x + 4, y + 2))

    def desenhar_hamburguer(self, cx, base_y, camadas, larg=210, alt=24):
        for i, chave in enumerate(camadas):
            _, cor = INGREDIENTES[chave]
            r = pygame.Rect(0, 0, larg, alt)
            r.midbottom = (cx, base_y - i * alt)
            pygame.draw.rect(self.tela, cor, r, border_radius=6)
            pygame.draw.rect(self.tela, COR_BORDA, r, 2, border_radius=6)

    def desenhar_cliente(self, ret, cli):
        pygame.draw.rect(self.tela, COR_SLOT, ret, border_radius=16)
        pygame.draw.rect(self.tela, COR_BORDA, ret, 3, border_radius=16)
        if cli is None:
            self.texto(
                "Aguardando cliente...", 22, (155, 143, 130), ret.center, centro=True
            )
            return

        bolha = pygame.Rect(ret.x + 15, ret.y + 15, ret.w - 30, 112)
        pygame.draw.rect(self.tela, (238, 238, 236), bolha, border_radius=12)
        pygame.draw.rect(self.tela, (170, 160, 150), bolha, 2, border_radius=12)
        self.texto(
            cli.nome_prato, 21, COR_TEXTO, (bolha.centerx, bolha.y + 17),
            centro=True, negrito=True,
        )
        n = len(cli.pedido)
        larg = n * 40 + (n - 1) * 10
        ix = bolha.centerx - larg // 2
        for i, chave in enumerate(cli.pedido):
            self.desenhar_icone(chave, ix + i * 50, bolha.y + 42, 40, indice=i)

        cx, cy = ret.centerx, ret.y + 222
        pygame.draw.circle(self.tela, cli.cor_cabelo, (cx, cy), 52)
        pygame.draw.circle(self.tela, cli.cor_pele, (cx, cy + 9), 46)
        pygame.draw.circle(self.tela, COR_BORDA, (cx, cy + 2), 52, 3)
        for olho in (-17, 17):
            pygame.draw.circle(self.tela, (40, 32, 28), (cx + olho, cy + 4), 6)
        pontos = []
        for i in range(9):
            x = cx - 18 + 36 * i / 8
            y = cy + 16 + math.sin(math.pi * i / 8) * 9
            pontos.append((x, y))
        pygame.draw.lines(self.tela, (120, 60, 50), False, pontos, 3)

        self.texto(cli.nome, 17, COR_TEXTO, (ret.centerx, ret.y + 288), centro=True)

        barra = pygame.Rect(ret.x + 45, ret.y + 305, ret.w - 90, 24)
        frac = max(0.0, cli.paciencia / cli.paciencia_max)
        if frac > 0.5:
            cor_frac = COR_VERDE
        elif frac > 0.25:
            cor_frac = COR_AMARELO
        else:
            cor_frac = COR_VERMELHO
        pygame.draw.rect(self.tela, (222, 216, 206), barra, border_radius=8)
        fill = int((barra.w - 6) * frac)
        if fill > 0:
            pygame.draw.rect(
                self.tela, cor_frac, (barra.x + 3, barra.y + 3, fill, barra.h - 6),
                border_radius=6,
            )
        pygame.draw.rect(self.tela, COR_BORDA, barra, 2, border_radius=8)

    def desenhar_hud(self):
        pygame.draw.rect(self.tela, COR_HUD, (0, 0, LARGURA, 56))
        branco = (250, 246, 240)
        self.texto(f"Dinheiro: ${self.dinheiro}", 25, branco, (16, 13), negrito=True)
        centro = f"Dia {self.dia}   |   {self.atendidos}/{self.meta} atendidos"
        self.texto(centro, 25, branco, (LARGURA // 2, 28), centro=True, negrito=True)
        img = self.f(25, True).render(
            f"Perdas: {self.perdas}/{MAX_PERDAS}", True, branco
        )
        self.tela.blit(img, img.get_rect(topright=(LARGURA - 16, 13)))

    def desenhar_bancada(self, esperados):
        pygame.draw.rect(self.tela, COR_BANCADA, RET_BANCADA)
        pygame.draw.rect(self.tela, COR_BANCADA_ESC, (0, 430, LARGURA, 7))

        self.texto("Seu prato", 22, (255, 250, 240), (230, 448), centro=True, negrito=True)
        if self.prato:
            if esperados:
                prox = " ou ".join(
                    INGREDIENTES[k][0] for k in sorted(esperados)
                )
                hint = f"Proximo: {prox}"
                cor_hint = (255, 235, 180)
            else:
                hint = "Pronto! Clique em SERVIR"
                cor_hint = (170, 255, 190)
        else:
            hint = "Clique nos ingredientes ao lado"
            cor_hint = (255, 235, 200)
        self.texto(hint, 18, cor_hint, (230, 476), centro=True)

        prato_ret = pygame.Rect(0, 0, 290, 52)
        prato_ret.center = (230, 660)
        pygame.draw.ellipse(self.tela, (250, 250, 250), prato_ret)
        pygame.draw.ellipse(self.tela, (175, 175, 175), prato_ret, 3)

        if not self.prato:
            self.texto("(vazio)", 20, (215, 205, 190), (230, 560), centro=True)
        else:
            for i, chave in enumerate(self.prato):
                _, cor = INGREDIENTES[chave]
                r = pygame.Rect(0, 0, 210, 22)
                r.midbottom = (230, 650 - i * 22)
                pygame.draw.rect(self.tela, cor, r, border_radius=5)
                pygame.draw.rect(self.tela, COR_BORDA, r, 2, border_radius=5)

        mouse = pygame.mouse.get_pos()
        for chave, ret in BOTOES:
            nome, cor = INGREDIENTES[chave]
            hover = ret.collidepoint(mouse)
            pygame.draw.rect(
                self.tela, COR_BOTAO_HOVER if hover else COR_BOTAO, ret,
                border_radius=10,
            )
            destacado = chave in esperados
            pygame.draw.rect(
                self.tela, COR_VERDE if destacado else COR_BORDA, ret,
                4 if destacado else 3, border_radius=10,
            )
            ic = pygame.Rect(ret.x + 12, ret.y + 20, 30, 30)
            pygame.draw.rect(self.tela, cor, ic, border_radius=5)
            pygame.draw.rect(self.tela, COR_BORDA, ic, 2, border_radius=5)
            self.texto(nome, 20, COR_TEXTO, (ret.x + 54, ret.centery), centro=True)

        serv_hover = RET_SERVIR.collidepoint(mouse)
        pygame.draw.rect(
            self.tela, COR_VERDE_ESC if serv_hover else COR_VERDE, RET_SERVIR,
            border_radius=10,
        )
        self.texto("SERVIR", 30, (255, 255, 255), RET_SERVIR.center, centro=True, negrito=True)

        lim_hover = RET_LIMPAR.collidepoint(mouse)
        pygame.draw.rect(
            self.tela, (178, 173, 166) if lim_hover else (204, 199, 192),
            RET_LIMPAR, border_radius=10,
        )
        self.texto("LIMPAR", 24, (60, 55, 50), RET_LIMPAR.center, centro=True, negrito=True)

        if self.msg is not None and self.msg_t > 0:
            s, cor = self.msg
            self.texto(s, 20, cor, (LARGURA // 2, 706), centro=True, negrito=True)

    def desenhar_jogo(self):
        self.tela.fill(COR_FUNDO)
        self.desenhar_hud()
        esperados = self.esperados()
        for ret, cli in zip(RET_SLOTS, self.clientes):
            self.desenhar_cliente(ret, cli)
        self.desenhar_bancada(esperados)

    def painel(self, titulo, cor_titulo, linhas):
        dim = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        dim.fill((25, 18, 12, 170))
        self.tela.blit(dim, (0, 0))
        p = pygame.Rect((LARGURA - 640) // 2, 155, 640, 410)
        pygame.draw.rect(self.tela, (252, 247, 238), p, border_radius=20)
        pygame.draw.rect(self.tela, COR_BORDA, p, 4, border_radius=20)
        self.texto(titulo, 46, cor_titulo, (p.centerx, p.y + 52), centro=True, negrito=True)
        y = p.y + 110
        for s, tam, cor, neg in linhas:
            self.texto(s, tam, cor, (p.centerx, y), centro=True, negrito=neg)
            y += tam + 22

    def desenhar_dia_completo(self):
        self.painel(
            f"DIA {self.dia} CONCLUIDO!",
            COR_VERDE,
            [
                (f"Todos os {self.meta} clientes foram atendidos.", 24, COR_TEXTO, False),
                (f"Bonus do dia: +${self.bonus}", 28, COR_VERDE_ESC, True),
                (f"Dinheiro total: ${self.dinheiro}", 24, COR_TEXTO, False),
                (f"Proximo: dia {self.dia + 1} - a paciencia vai diminuir", 22, (150, 95, 40), False),
                ("Clique para continuar", 26, COR_VERDE, True),
            ],
        )

    def desenhar_fim(self):
        self.painel(
            "FIM DE JOGO",
            COR_VERMELHO,
            [
                (f"Voce perdeu {MAX_PERDAS} clientes no dia {self.dia}.", 24, COR_TEXTO, False),
                (f"Dinheiro total: ${self.dinheiro}", 30, COR_VERDE_ESC, True),
                (f"Dias completos: {max(0, self.dia - 1)}", 24, (100, 85, 75), False),
                ("Clique para jogar novamente", 26, COR_VERDE, True),
            ],
        )

    def desenhar_titulo(self):
        self.tela.fill(COR_FUNDO)
        pygame.draw.rect(self.tela, COR_BANCADA, (0, 650, LARGURA, 70))
        pygame.draw.rect(self.tela, COR_BANCADA_ESC, (0, 650, LARGURA, 7))

        camadas = ["pao", "carne", "queijo", "alface", "tomate", "pao"]
        self.desenhar_hamburguer(LARGURA // 2, 340, camadas, larg=240, alt=26)

        self.texto("LANCHES DO CHEFE", 60, COR_TEXTO, (480, 410), centro=True, negrito=True)
        self.texto(
            "Monte os hamburgueres na ordem e sirva antes da paciencia acabar!",
            23, (95, 78, 66), (480, 468), centro=True,
        )
        self.texto(
            "Clique nos ingredientes, acerte a ordem e clique em SERVIR",
            20, (130, 108, 92), (480, 505), centro=True,
        )
        self.texto(
            f"Errou o ingrediente = prato zerado   |   {MAX_PERDAS} clientes perdidos = fim de jogo",
            20, (130, 108, 92), (480, 538), centro=True,
        )
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.texto(
                "Clique para comecar", 30, COR_VERDE, (480, 610), centro=True, negrito=True
            )

    def desenhar(self):
        if self.estado == "titulo":
            self.desenhar_titulo()
            return
        self.desenhar_jogo()
        if self.estado == "dia_completo":
            self.desenhar_dia_completo()
        elif self.estado == "fim":
            self.desenhar_fim()

    # ---------- loop ----------

    def rodar(self):
        while True:
            dt = self.relogio.tick(FPS) / 1000.0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.clique(ev.pos)
            if self.estado == "jogando":
                self.atualizar(dt)
            self.desenhar()
            pygame.display.flip()


def main():
    pygame.init()
    try:
        Jogo().rodar()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
