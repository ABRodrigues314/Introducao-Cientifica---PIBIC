"""
Esse arquivo instroduz funções de busca sobre informações do pubmed e coloca agentes de LLM para 
criar um relatório completo do assunto em questão
"""

from buscar import validar_argumentos, buscar_ids, buscar_conteudo, extrair_titulo, extrair_pubmedid, extrair_resumo, extrair_resumo_completo

__all__ = [validar_argumentos, buscar_ids, buscar_conteudo, extrair_titulo, extrair_pubmedid, extrair_resumo, extrair_resumo_completo]

__version__ = "1.0"