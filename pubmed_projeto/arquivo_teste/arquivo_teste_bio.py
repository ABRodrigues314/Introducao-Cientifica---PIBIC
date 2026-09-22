"""
Esse arquivo foi criado usando Gemini, para fins didáticos
"""

from Bio import Entrez

# 1. IDENTIFICAÇÃO OBRIGATÓRIA
# O NCBI (mantenedor do PubMed) exige que você forneça seu e-mail para usar a API.
Entrez.email = "blotarodriguesabner@gmail.com"


def buscar_pmids(termo_busca, max_resultados=5):
    """Busca no PubMed e retorna uma lista de IDs (PMIDs) de artigos."""
    handle = Entrez.esearch(
        db="pubmed", term=termo_busca, retmax=max_resultados, sort="relevance"
    )
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def obter_abstracts(pmid_list):
    """Dado uma lista de PMIDs, busca e extrai os títulos e resumos (abstracts)."""
    if not pmid_list:
        return []

    # Faz o download das informações dos artigos em formato XML
    handle = Entrez.efetch(
        db="pubmed", id=",".join(pmid_list), rettype="xml", retmode="xml"
    )
    records = Entrez.read(handle)
    handle.close()

    artigos = []

    # O formato retornado é um dicionário XML estruturado do NCBI
    for pubmed_article in records["PubmedArticle"]:
        medline = pubmed_article["MedlineCitation"]

        # Extrai o ID e o Título
        pmid = str(medline["PMID"])
        titulo = medline["Article"]["ArticleTitle"]

        # Extrai o Abstract (se existir)
        abstract_text = ""
        if "Abstract" in medline["Article"]:
            # Alguns abstracts são divididos em seções (Background, Methods, Results, etc.)
            abstract_parts = medline["Article"]["Abstract"]["AbstractText"]
            abstract_text = " ".join(abstract_parts)
        else:
            abstract_text = "Resumo não disponível."

        artigos.append({"pmid": pmid, "titulo": titulo, "abstract": abstract_text})

    return artigos


# --- EXEMPLO DE USO ---
termo = "Wolbachia dengue"
print(f"Buscando artigos para: '{termo}'...\n")

# 1. Obtém os IDs dos artigos mais relevantes
ids = buscar_pmids(termo_busca=termo, max_resultados=3)

# 2. Busca e exibe os resumos
resultados = obter_abstracts(ids)

for i, artigo in enumerate(resultados, 1):
    print(f"--- ARTIGO {i} (PMID: {artigo['pmid']}) ---")
    print(f"Título: {artigo['titulo']}")
    print(f"Abstract:\n{artigo['abstract']}\n")