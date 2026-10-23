# Lanches do Chefe

Jogo de restaurante simples em Python + Pygame. Você é o chef de uma
lanchonete: monte os hambúrgueres na ordem certa e sirva os clientes
antes que a paciência deles acabe.

## Como jogar

1. Clique para começar.
2. Veja o pedido do cliente (os ingredientes aparecem na ordem de montagem).
3. Clique nos ingredientes **na ordem certa** — errar zera o prato.
4. Clique em **SERVIR** para entregar o prato certo ao cliente certo.
5. Quanto mais rápido servir, maior o bônus de paciência.

- **LIMPAR**: zera o prato atual sem penalidade.
- Ingredientes válidos para o pedido atual são destacados com borda verde.
- A cada dia completo há bônus em dinheiro e a paciência diminui.
- Perder **3 clientes no mesmo dia** encerra o jogo.

## Como rodar

Requer Python 3.10+ e `pygame-ce` (já instalado no ambiente).

```
python jogo.py
```
