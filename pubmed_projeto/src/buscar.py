"""
Esse módulo busca criar funções mais práticas 0de busca baseado
nas funções já estabelecidas no módulo Bio.Entrez
"""

from Bio import Entrez

from erros import LimiteExcedidoError

Entrez.email = "blotarodriguesa@gmail.com"

# Conversar sobre docstring
# Funções de validação --------------------------------------

def _validar_argumentos(tema_ids: str, numero_de_ids=5, ordem="relevance"):
    """Valida os argumentos recebidos pelas funções de busca.

    Essa função busca validar se os parâmetros são válidos para serem usados. Primeiro verifica-se
    o tipo dos parâmetros, depois verifica-se o limite de ids e, por fim, se o parâmetro ordem é
    válida.

    Args:
        tema_ids (str): Tema ou termo de busca a ser pesquisado no PubMed.
        numero_de_ids (int, optional): Quantidade máxima de ids a serem retornados. Deve ser
            menor ou igual a 300. Defaults to 5.
        ordem (str, optional): Critério de ordenação dos resultados. Deve ser um entre
            ``"relevance"``, ``"pub_data"``, ``"Author"`` ou ``"JournalName"``.
            Defaults to "relevance".

    Returns:
        None: A função não retorna valor; apenas valida os argumentos.

    Raises:
        TypeError: Se algum dos parâmetros não for do tipo esperado.
        LimiteExcedidoError: Se ``numero_de_ids`` for maior que 300.
        ValueError: Se ``ordem`` não for um dos critérios de ordenação permitidos.
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

def _buscar_ids(tema_ids: str, numero_de_ids=5, ordem="relevance") -> list:
    """Busca ids de artigos no PubMed a partir de um tema.

    Essa função recebe um tema e um número de linha e busca,
    no pubmed, e busca vários ids com o conteúdo baseado no
    tema pedido.

    Args:
        tema_ids (str): Tema ou termo de busca a ser pesquisado no PubMed.
        numero_de_ids (int, optional): Quantidade máxima de ids a serem retornados.
            Defaults to 5.
        ordem (str, optional): Critério de ordenação dos resultados.
            Defaults to "relevance".

    Returns:
        list: Lista com os ids (strings) dos artigos encontrados.

    Raises:
        TypeError: Se algum dos parâmetros não for do tipo esperado.
        LimiteExcedidoError: Se ``numero_de_ids`` for maior que 300.
        ValueError: Se ``ordem`` não for um critério de ordenação permitido.
    """

    _validar_argumentos(tema_ids, numero_de_ids, ordem)

    conexao_ids = Entrez.esearch(
        db = "pubmed", term=tema_ids, retmax=numero_de_ids, sort=ordem
    )

    lista_ids = Entrez.read(conexao_ids)

    conexao_ids.close()

    return lista_ids["IdList"]

def _buscar_conteudo(lista_ids: list) -> dict:
    """Busca o conteúdo completo dos artigos a partir de uma lista de ids.

    Essa função recebe uma lista de ids e, no data base do PubMed,
    busca os resumos referentes aos ids.

    Args:
        lista_ids (list): Lista com os ids (strings) dos artigos a serem buscados.

    Returns:
        dict | list: Estrutura retornada pelo ``Entrez.read`` contendo os dados dos
        artigos (normalmente um dicionário com a chave ``"PubmedArticle"``). Caso
        ``lista_ids`` seja uma lista vazia, retorna uma lista vazia.

    Raises:
        Exception: Erros levantados pela comunicação ou leitura dos dados do PubMed.
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

def _extrair_titulo(conteudo: dict) -> list:
    """Extrai os títulos dos artigos de um conteúdo do PubMed.

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o título
    do artigo em questão.

    Args:
        conteudo (dict): Dicionário com os dados dos artigos, contendo a chave
            ``"PubmedArticle"``.

    Returns:
        list: Lista com os títulos (strings) dos artigos, na ordem em que aparecem
        no conteúdo.

    Raises:
        KeyError: Se alguma das chaves esperadas não existir no dicionário recebido.
    """
    artigos = conteudo["PubmedArticle"]
    lista_titulos = []
    for artigo in artigos:
        lista_titulos.append(artigo["MedlineCitation"]["Article"]["ArticleTitle"])

    return lista_titulos

def _extrair_pubmedid(conteudo: dict) -> str:
    """Extrai os identificadores (PMID) dos artigos de um conteúdo do PubMed.

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o Id
    do artigo em questão.

    Args:
        conteudo (dict): Dicionário com os dados dos artigos, contendo a chave
            ``"PubmedArticle"``.

    Returns:
        list: Lista com os identificadores PMID dos artigos, na ordem em que
        aparecem no conteúdo.

    Raises:
        KeyError: Se alguma das chaves esperadas não existir no dicionário recebido.
    """
    artigos = conteudo["PubmedArticle"]
    lista_ids = []

    for artigo in artigos:
        lista_ids.append(artigo["MedlineCitation"]["PMID"])

    return lista_ids

def _extrair_resumo(conteudo: dict) -> str:
    """Extrai os resumos dos artigos de um conteúdo do PubMed.

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o resumo
    do artigo em questão.

    Args:
        conteudo (dict): Dicionário com os dados dos artigos, contendo a chave
            ``"PubmedArticle"``. Cada artigo pode ou não possuir a chave ``"Abstract"``.

    Returns:
        list: Lista com os resumos (strings) dos artigos. Quando o resumo é composto
        por várias partes, elas são concatenadas com espaços. Quando não há resumo
        disponível, é usada a string ``"Resumo não disponível"``.

    Raises:
        KeyError: Se alguma das chaves esperadas não existir no dicionário recebido.
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
                lista_resumos.append(texto)
        else:
            lista_resumos.append("Resumo não disponível")

    return lista_resumos

def _extrair_resumo_completo(conteudo: dict) -> dict:
    """Reúne título, identificador e resumo de cada artigo em um único dicionário.

    Esse artigo recebe o conteudo de um artigo em forma de dicionário e extrai o título,
    Id e o resumo do arquivo em questão, juntando essas três informações em um novo dicionário.

    Args:
        conteudo (dict): Dicionário com os dados dos artigos, contendo a chave
            ``"PubmedArticle"``.

    Returns:
        dict: Dicionário com as chaves ``"Título"``, ``"Id"`` e ``"Resumo"``, cada
        uma contendo uma lista com as informações correspondentes aos artigos.

    Raises:
        KeyError: Se alguma das chaves esperadas não existir no dicionário recebido.
    """
    resumo_completo = {}
    resumo_completo["Título"] = _extrair_titulo(conteudo)
    resumo_completo["Id"] = _extrair_pubmedid(conteudo)
    resumo_completo["Resumo"] = _extrair_resumo(conteudo)    
    return resumo_completo

# Função main() --------------------------------------

def procurar_resumos(tema: str, quantidade=5, ordem="relevance", imprimir=True) -> dict:
    """Executa a busca e a extração de resumos do PubMed para um tema.

    Essa função executa todas as funções em uma ordem específica, visando testar todas as
    funcionalidades do arquivo. Nesse caso, buscamos dez resumos sobre o Alzheimer e imprimimos
    no terminal

    Args:
        tema (str): Tema ou termo de busca a ser pesquisado no PubMed.
        quantidade (int, optional): Quantidade máxima de resumos a serem buscados.
            Defaults to 5.
        ordem (str, optional): Critério de ordenação dos resultados.
            Defaults to "relevance".
        imprimir (bool, optional): Se ``True``, imprime os resumos encontrados no
            terminal. Defaults to True.

    Returns:
        dict: Dicionário com as chaves ``"Título"``, ``"Id"`` e ``"Resumo"``, cada
        uma contendo uma lista com as informações correspondentes aos artigos.

    Raises:
        TypeError: Se algum dos parâmetros de busca não for do tipo esperado.
        LimiteExcedidoError: Se ``quantidade`` for maior que 300.
        ValueError: Se ``ordem`` não for um critério de ordenação permitido.
    """
    lista_de_ids = _buscar_ids(tema, quantidade,ordem)
    conteudo = _buscar_conteudo(lista_de_ids)
    resumos = _extrair_resumo_completo(conteudo)

    if imprimir:
        titulos = resumos["Título"]
        id = resumos["Id"]
        resumo = resumos["Resumo"]

        for numero_resumo in range(len(titulos)):
            print("_"*80)
            print("Título:",titulos[numero_resumo])
            print("\nId:",id[numero_resumo])
            print("\nResumo:",resumo[numero_resumo])
            print("_"*80)

    return resumos

# __main__ --------------------------------------

if __name__ == "__main__":
    procurar_resumos("Alzheimer", 5)
