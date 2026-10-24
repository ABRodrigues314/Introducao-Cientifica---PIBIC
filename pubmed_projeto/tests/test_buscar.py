"""
Ambiente de testes do módulo buscar
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pubmed_projeto.src.buscar import _validar_argumentos, _buscar_conteudo, _buscar_ids, _extrair_pubmedid, _extrair_resumo, _extrair_resumo_completo, _extrair_titulo, procurar_resumos
from pubmed_projeto.src.erros import LimiteExcedidoError


def _conteudo_exemplo():
    """Monta uma estrutura de conteúdo semelhante à retornada pelo Entrez."""
    return {
        "PubmedArticle": [
            {
                "MedlineCitation": {
                    "PMID": "111",
                    "Article": {
                        "ArticleTitle": "Título do primeiro artigo",
                        "Abstract": {"AbstractText": ["Parte um", "Parte dois"]},
                    },
                }
            },
            {
                "MedlineCitation": {
                    "PMID": "222",
                    "Article": {
                        "ArticleTitle": "Título do segundo artigo",
                    },
                }
            },
            {
                "MedlineCitation": {
                    "PMID": "333",
                    "Article": {
                        "ArticleTitle": "Título do terceiro artigo",
                        "Abstract": {"AbstractText": "Resumo em texto único"},
                    },
                }
            },
        ]
    }


class TestValidarArgumentos(unittest.TestCase):
    """Testes da função _validar_argumentos."""

    def test_argumentos_validos_nao_levantam_erro(self):
        _validar_argumentos("Alzheimer", numero_de_ids=5, ordem="relevance")

    def test_tema_ids_diferente_de_str(self):
        with self.assertRaises(TypeError):
            _validar_argumentos(123, numero_de_ids=5)

    def test_tipos_ids_diferente_de_int(self):
        with self.assertRaises(TypeError):
            _validar_argumentos("Alzheimer", numero_de_ids="5")

    def test_ordem_diferente_de_str(self):
        with self.assertRaises(TypeError):
            _validar_argumentos("Alzheimer", numero_de_ids=5, ordem=["relevance"])

    def test_limite_de_ids_excedido(self):
        with self.assertRaises(LimiteExcedidoError):
            _validar_argumentos("Alzheimer", numero_de_ids=301)

    def test_limite_de_ids_no_valor_maximo(self):
        _validar_argumentos("Alzheimer", numero_de_ids=300)

    def test_ordem_invalida(self):
        with self.assertRaises(ValueError):
            _validar_argumentos("Alzheimer", numero_de_ids=5, ordem="data")

    def test_todas_as_ordens_validas(self):
        for ordem in ["relevance", "pub_data", "Author", "JournalName"]:
            with self.subTest(ordem=ordem):
                _validar_argumentos("Alzheimer", numero_de_ids=5, ordem=ordem)


class TestBuscarIds(unittest.TestCase):
    """Testes da função _buscar_ids."""

    @patch("pubmed_projeto.src.buscar.Entrez.read")
    @patch("pubmed_projeto.src.buscar.Entrez.esearch")
    def test_retorna_lista_de_ids_e_fecha_conexao(self, mock_esearch, mock_read):
        conexao = MagicMock()
        mock_esearch.return_value = conexao
        mock_read.return_value = {"IdList": ["111", "222"]}

        resultado = _buscar_ids("Alzheimer", 2, "relevance")

        self.assertEqual(resultado, ["111", "222"])
        mock_esearch.assert_called_once_with(
            db="pubmed", term="Alzheimer", retmax=2, sort="relevance"
        )
        mock_read.assert_called_once_with(conexao)
        conexao.close.assert_called_once()

    @patch("pubmed_projeto.src.buscar.Entrez.esearch")
    def test_argumento_invalido_nao_realiza_busca(self, mock_esearch):
        with self.assertRaises(TypeError):
            _buscar_ids("Alzheimer", "2")

        mock_esearch.assert_not_called()

    @patch("pubmed_projeto.src.buscar.Entrez.esearch")
    def test_limite_excedido_nao_realiza_busca(self, mock_esearch):
        with self.assertRaises(LimiteExcedidoError):
            _buscar_ids("Alzheimer", 301)

        mock_esearch.assert_not_called()


class TestBuscarConteudo(unittest.TestCase):
    """Testes da função _buscar_conteudo."""

    def test_lista_vazia_retorna_lista_vazia(self):
        self.assertEqual(_buscar_conteudo([]), [])

    @patch("pubmed_projeto.src.buscar.Entrez.read")
    @patch("pubmed_projeto.src.buscar.Entrez.efetch")
    def test_busca_conteudo_e_fecha_conexao(self, mock_efetch, mock_read):
        conexao = MagicMock()
        conteudo = _conteudo_exemplo()
        mock_efetch.return_value = conexao
        mock_read.return_value = conteudo

        resultado = _buscar_conteudo(["111", "222"])

        self.assertEqual(resultado, conteudo)
        mock_efetch.assert_called_once_with(
            db="pubmed", id="111,222", rettype="xml", retmode="xml"
        )
        mock_read.assert_called_once_with(conexao)
        conexao.close.assert_called_once()


class TestExtrairTitulo(unittest.TestCase):
    """Testes da função _extrair_titulo."""

    def test_extrai_titulos_na_ordem(self):
        resultado = _extrair_titulo(_conteudo_exemplo())

        self.assertEqual(
            resultado,
            [
                "Título do primeiro artigo",
                "Título do segundo artigo",
                "Título do terceiro artigo",
            ],
        )

    def test_conteudo_sem_chave_esperada(self):
        with self.assertRaises(KeyError):
            _extrair_titulo({})


class TestExtrairPubmedid(unittest.TestCase):
    """Testes da função _extrair_pubmedid."""

    def test_extrai_ids_na_ordem(self):
        resultado = _extrair_pubmedid(_conteudo_exemplo())

        self.assertEqual(resultado, ["111", "222", "333"])

    def test_conteudo_sem_chave_esperada(self):
        with self.assertRaises(KeyError):
            _extrair_pubmedid({})


class TestExtrairResumo(unittest.TestCase):
    """Testes da função _extrair_resumo."""

    def test_extrai_resumos_concatenados_unicos_e_ausentes(self):
        resultado = _extrair_resumo(_conteudo_exemplo())

        self.assertEqual(
            resultado,
            [
                "Parte um Parte dois",
                "Resumo não disponível",
                "Resumo em texto único",
            ],
        )

    def test_conteudo_sem_chave_esperada(self):
        with self.assertRaises(KeyError):
            _extrair_resumo({})


class TestExtrairResumoCompleto(unittest.TestCase):
    """Testes da função _extrair_resumo_completo."""

    def test_retorna_dicionario_com_titulos_ids_e_resumos(self):
        resultado = _extrair_resumo_completo(_conteudo_exemplo())

        self.assertEqual(
            set(resultado.keys()), {"Título", "Id", "Resumo"}
        )
        self.assertEqual(
            resultado["Título"],
            [
                "Título do primeiro artigo",
                "Título do segundo artigo",
                "Título do terceiro artigo",
            ],
        )
        self.assertEqual(resultado["Id"], ["111", "222", "333"])
        self.assertEqual(
            resultado["Resumo"],
            [
                "Parte um Parte dois",
                "Resumo não disponível",
                "Resumo em texto único",
            ],
        )


class TestProcurarResumos(unittest.TestCase):
    """Testes da função procurar_resumos."""

    @patch("pubmed_projeto.src.buscar._extrair_resumo_completo")
    @patch("pubmed_projeto.src.buscar._buscar_conteudo")
    @patch("pubmed_projeto.src.buscar._buscar_ids")
    def test_executa_fluxo_completo_sem_imprimir(
        self, mock_buscar_ids, mock_buscar_conteudo, mock_extrair
    ):
        mock_buscar_ids.return_value = ["111"]
        mock_buscar_conteudo.return_value = {"PubmedArticle": []}
        esperado = {"Título": ["Título"], "Id": ["111"], "Resumo": ["Resumo"]}
        mock_extrair.return_value = esperado

        resultado = procurar_resumos("Alzheimer", 1, "Author", imprimir=False)

        self.assertEqual(resultado, esperado)
        mock_buscar_ids.assert_called_once_with("Alzheimer", 1, "Author")
        mock_buscar_conteudo.assert_called_once_with(["111"])
        mock_extrair.assert_called_once_with({"PubmedArticle": []})

    @patch("pubmed_projeto.src.buscar._extrair_resumo_completo")
    @patch("pubmed_projeto.src.buscar._buscar_conteudo")
    @patch("pubmed_projeto.src.buscar._buscar_ids")
    def test_imprime_resumos_quando_solicitado(
        self, mock_buscar_ids, mock_buscar_conteudo, mock_extrair
    ):
        mock_buscar_ids.return_value = ["111"]
        mock_buscar_conteudo.return_value = {"PubmedArticle": []}
        mock_extrair.return_value = {
            "Título": ["Título de teste"],
            "Id": ["111"],
            "Resumo": ["Resumo de teste"],
        }

        saida = io.StringIO()
        with redirect_stdout(saida):
            procurar_resumos("Alzheimer", 1)

        texto = saida.getvalue()
        self.assertIn("Título de teste", texto)
        self.assertIn("111", texto)
        self.assertIn("Resumo de teste", texto)


if __name__ == "__main__":
    unittest.main()
