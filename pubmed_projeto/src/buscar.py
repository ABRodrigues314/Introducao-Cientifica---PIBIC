"""
Esse módulo busca criar funções mais práticas 0de busca baseado
nas funções já estabelecidas no módulo Bio.Entrez
"""

from Bio import Entrez
from erros import LimiteExcedidoError

Entrez.email = "blotarodriguesa@gmail.com"

# Conversar sobre docstring
# Funções de validação --------------------------------------

def validar_argumentos(tema_ids: str, numero_de_ids=5, ordem="relevance"):
    """Função que valida o input de buscar_ids.
    
    Essa função busca validar se os parâmetros são válidos para serem usados. Primeiro verifica-se
    o tipo dos parâmetros, depois verifica-se o limite de ids e, por fim, se o parâmetro ordem é 
    válida.

    Args:

    Returns:

    Raises:
    """
    if not type(numero_de_ids) == int or not type(tema_ids) == str or not type(ordem) == str:
            # Verificando se os tipos dos argumentos estão corretos
            raise TypeError("O tipo de algum dos parâmetros está errado! tema_ids: str, numero_de_ids: int, ordem: str") # conversar TypeError
    
    if numero_de_ids > 300:
        # Verificando se o limite de número de ids está sendo repeitado
        raise LimiteExcedidoError("O limite de números de ids é 300")
    
    if ordem not in ["relevance","pub_data","Author","JournalName"]:
        # verificando se o parâmetro ordem é válido
        raise ValueError("A ordem deve ser relevance, pub_data, Author ou JournalName.") # conversar ValueError

# Funções de busca --------------------------------------

def buscar_ids(tema_ids: str, numero_de_ids=5, ordem="relevance") -> list:
    """Função de busca de ids

    Essa função recebe um tema e um número de linha e busca,
    no pubmed, e busca vários ids com o conteúdo baseado no
    tema pedido.

    Args:

    Returns:

    Raises:
    """

    validar_argumentos(tema_ids, numero_de_ids, ordem)

    conexao_ids = Entrez.esearch(
        db = "pubmed", term=tema_ids, retmax=numero_de_ids, sort=ordem
    )

    lista_ids = Entrez.read(conexao_ids)

    conexao_ids.close()

    return lista_ids["IdList"]

def buscar_conteudo(lista_ids: list) -> dict:
    """Função de extração de resumos
    
    Essa função recebe uma lista de ids e, no data base do PubMed,
    busca os resumos referentes aos ids.

    Args:

    Returns:

    Raises:
    """

    if lista_ids == []:
        return []

    conexao_artigo = Entrez.efetch(
         db="pubmed", id=",".join(lista_ids), rettype="xml", retmode="xml"
    )    

    informacoes_arquivo = Entrez.read(conexao_artigo)

    conexao_artigo.close()

    return informacoes_arquivo

# Funções de extração --------------------------------------

def extrair_titulo(conteudo: dict) -> list:
    """
    Função de extração de título

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o título
    do artigo em questão.

    Args:

    Returns:

    Raises:    
    """
    artigos = conteudo["PubmedArticle"]
    lista_titulos = []
    for artigo in artigos:
        lista_titulos.append(artigo["MedlineCitation"]["Article"]["ArticleTitle"])

    return lista_titulos

def extrair_pubmedid(conteudo: dict) -> str:
    """Função de extração de Id

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o Id
    do artigo em questão.

    Args:

    Returns:

    Raises:    
    """
    artigos = conteudo["PubmedArticle"]
    lista_ids = []

    for artigo in artigos:
        lista_ids.append(artigo["MedlineCitation"]["PMID"])

    return lista_ids

def extrair_resumo(conteudo: dict) -> str:
    """Função de extração de resumo

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o resumo
    do artigo em questão.

    Args:

    Returns:

    Raises:    
    """
    artigos = conteudo["PubmedArticle"]
    lista_resumos = []
    for artigo in artigos:
        medline_article = artigo["MedlineCitation"]["Article"]
        if "Abstract" in medline_article:
            texto = medline_article["Abstract"]["AbstractText"]
            if type(texto) == list:
                texto_concatenado = " ".join(texto)
                lista_resumos.append(texto_concatenado)
            else:
                lista_resumos(texto)
        else:
            lista_resumos.append("Resumo não disponível")

    return lista_resumos

def extrair_resumo_completo(conteudo: dict) -> dict:
    """Função de extração de resumo completo

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o título,
    Id e o resumo do arquivo em questão, juntando essas três informações em um novo dicionário.
    

    Args:

    Returns:

    Raises:    
    """
    resumo_completo = {}
    resumo_completo["Título"] = extrair_titulo(conteudo)
    resumo_completo["Id"] = extrair_pubmedid(conteudo)
    resumo_completo["Resumo"] = extrair_resumo(conteudo)    
    return resumo_completo

# Função main() --------------------------------------

def main(tema: str, quantidade=5, ordem="relevance"):
    """Função main do projeto

    Essa função executa todas as funções em uma ordem específica, visando testar todas as 
    funcionalidades do arquivo. Nesse caso, buscamos dez resumos sobre o Alzheimer e imprimimos
    no terminal

    Args:

    Returns:

    Raises:
    """
    lista_de_ids = buscar_ids(tema, quantidade,ordem)
    conteudo = buscar_conteudo(lista_de_ids)
    resumos = extrair_resumo_completo(conteudo)

    titulos = resumos["Título"]
    id = resumos["Id"]
    resumo = resumos["Resumo"]

    # Alerta de Gambiarra (no range(len(titulos)))
    for numero_resumo in range(len(titulos)):
        print("_"*80)
        print("Título:",titulos[numero_resumo])
        print("\nId:",id[numero_resumo])
        print("\nResumo:",resumo[numero_resumo])
        print("_"*80)


# __main__ --------------------------------------

if __name__ == "__main__":
    main("Alzheimer", 5)