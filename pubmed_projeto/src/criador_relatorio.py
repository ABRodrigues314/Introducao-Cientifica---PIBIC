"""
Esse módulo é usado para criar relatórios baseados em um conjunto de resumos.
A LLM usada nessa fase de teste é o Gemini.
Atenção: esse arquivo foi feito para testes e chave de api não deve ser exposta na variável api_key
caso o arquivo com a chave se torne público.
(O módulo está incompleto ainda)
"""

from pubmed_projeto.src.buscar import procurar_resumos
from google import genai
from pubmed_projeto.src.erros import ChaveInvalidaError
from docx import Document

chave_api = "SUA_CHAVE"
modelo_gemini = "SEU_MODELO"

cliente = genai.Client(
    api_key=chave_api
)

def _validar_dados():
    """"""
    if chave_api == "SUA_CHAVE":
        raise ChaveInvalidaError("Você precisa colocar uma chave")

    if modelo_gemini == "SEU_MODELO":
        raise ChaveInvalidaError("Você precisa colocar um modelo")

    lista_modelos = []
    for modelo in cliente.models.list():
        lista_modelos.append(modelo.name)
    if f"models/{modelo_gemini}" not in lista_modelos:
        raise ChaveInvalidaError("Modelo inválido")

    return lista_modelos


def _gerar_resumo_inicial(resumos: dict, tema: str) -> str:
    """
    """
    _validar_dados()
    primeiros_resumos = resumos["Resumo"][0:3]
    primeiros_resumos = " // ".join(primeiros_resumos)
    prompt = f"""Atue como um especialista em {tema}. Escreva um resumo síntese de 240 a 320 palavras com base EXCLUSIVAMENTE nos resumos de artigos fornecidos abaixo. Não peça mais informações, apenas gere o texto final.

    Resumos dos artigos:
    {primeiros_resumos}"""
    resumo_inicial = cliente.models.generate_content(
        model=modelo_gemini,
        contents=prompt,
    )

    return resumo_inicial.text

def gerar_relatorio(tema: str, quantidade_resumos: int):
    """
    """
    document = Document()
    resumos = procurar_resumos(tema, 5, imprimir=False)
    resumo_inicial = _gerar_resumo_inicial(resumos, tema)
    document.add_heading(f"Relatório sobre {tema}", 0)
    document.add_heading("Resumo Inicial", level=1)
    document.add_paragraph(resumo_inicial)
    document.add_heading("Resumos", level=1)
    for numero_resumo in range(len(resumos["Resumo"])):
        document.add_heading(resumos["Título"][numero_resumo], level=2)
        document.add_paragraph(resumos["Resumo"][numero_resumo])
    document.save(f"relatorio_{tema}.docx")

gerar_relatorio("Alzheimer", 5)

