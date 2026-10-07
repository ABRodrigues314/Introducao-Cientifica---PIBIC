"""
Esse arquivo instroduz funções de busca sobre informações do pubmed e coloca agentes de LLM para 
criar um relatório completo do assunto em questão
"""

from pubmed_projeto.src.buscar import procurar_resumos

__all__ = [procurar_resumos]

__version__ = "1.0"