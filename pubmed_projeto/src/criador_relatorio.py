"""
Esse módulo é usado para criar relatórios baseados em um conjunto de resumos.
A LLM usada nessa fase de teste é o Gemini. 
Atenção: esse arquivo foi feito para testes e chave de api não deve ser exposta na variável api_key
caso o arquivo com a chave se torne público.
(O módulo está incompleto ainda)
"""

from pubmed_projeto.src.buscar import procurar_resumos
from google import generativeai as genai
from pubmed_projeto.src.erros import ChaveInvalidaError
from docx import Document

chave_api = "SUA_CHAVE"
modelo_gemini = "SEU_MODELO"

def _validar_dados():
    """"""
    if chave_api == "SUA_CHAVE":
        raise ChaveInvalidaError("Você precisa colocar uma chave")
    
    if modelo_gemini == "SEU_MODELO":
        pass

    # Verificar se existe o modelo

def _gerar_resumo_inicial(resumos: dict, tema: str):
    """"""
    titulos = resumos["Título"]
    titulos = " // ".join(titulos)
    resumo_inicial = modelo_escolhido.generate_content("Você é um especialista em {tema} e está trabalhando em um relatório sobre o assunto. " \
    "Esse relatório informa sobre alguns artigos selecionados, cujos temas estão entre os sinais <temas>. Você deverá criar um resumo inicial" \
    "sobre o tema com 240 até 320 palavras para esse relatório. Temas: <{titulos}>")

    return resumo_inicial
    
def gerar_relatorio():
    pass
    
genai.configure(api_key=chave_api)
modelo_escolhido = genai.GenerativeModel("gemini-3.5-flash")

