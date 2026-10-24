"""
Ambiente de testes do módulo criador_relatorio
"""

import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pubmed_projeto.src import criador_relatorio
from pubmed_projeto.src.erros import ChaveInvalidaError


class TestValidarDados(unittest.TestCase):
    """Testes da função _validar_dados."""

    def test_chave_padrao_levanta_erro(self):
        with patch.object(criador_relatorio, "chave_api", "SUA_CHAVE"):
            with self.assertRaises(ChaveInvalidaError):
                criador_relatorio._validar_dados()

    def test_modelo_padrao_levanta_erro(self):
        with patch.object(criador_relatorio, "chave_api", "chave-valida"):
            with patch.object(criador_relatorio, "modelo_gemini", "SEU_MODELO"):
                with self.assertRaises(ChaveInvalidaError):
                    criador_relatorio._validar_dados()

    def test_modelo_indisponivel_levanta_erro(self):
        cliente = MagicMock()
        cliente.models.list.return_value = [SimpleNamespace(name="models/outro-modelo")]

        with patch.object(criador_relatorio, "chave_api", "chave-valida"):
            with patch.object(criador_relatorio, "modelo_gemini", "gemini-pro"):
                with patch.object(criador_relatorio, "cliente", cliente):
                    with self.assertRaises(ChaveInvalidaError):
                        criador_relatorio._validar_dados()

    def test_dados_validos_retornam_lista_de_modelos(self):
        cliente = MagicMock()
        cliente.models.list.return_value = [
            SimpleNamespace(name="models/gemini-pro"),
            SimpleNamespace(name="models/outro-modelo"),
        ]

        with patch.object(criador_relatorio, "chave_api", "chave-valida"):
            with patch.object(criador_relatorio, "modelo_gemini", "gemini-pro"):
                with patch.object(criador_relatorio, "cliente", cliente):
                    resultado = criador_relatorio._validar_dados()

        self.assertEqual(
            resultado, ["models/gemini-pro", "models/outro-modelo"]
        )
        cliente.models.list.assert_called_once_with()


class TestGerarResumoInicial(unittest.TestCase):
    """Testes da função _gerar_resumo_inicial."""

    @patch.object(criador_relatorio, "_validar_dados")
    def test_retorna_texto_gerado_pelo_modelo(self, mock_validar):
        cliente = MagicMock()
        resposta = MagicMock()
        resposta.text = "Resumo síntese gerado"
        cliente.models.generate_content.return_value = resposta

        resumos = {"Resumo": ["r1", "r2", "r3", "r4"]}

        with patch.object(criador_relatorio, "cliente", cliente):
            with patch.object(criador_relatorio, "modelo_gemini", "gemini-pro"):
                resultado = criador_relatorio._gerar_resumo_inicial(
                    resumos, "Alzheimer"
                )

        self.assertEqual(resultado, "Resumo síntese gerado")
        mock_validar.assert_called_once_with()
        cliente.models.generate_content.assert_called_once()
        argumentos = cliente.models.generate_content.call_args.kwargs
        self.assertEqual(argumentos["model"], "gemini-pro")
        self.assertIn("Alzheimer", argumentos["contents"])
        self.assertIn("r1 // r2 // r3", argumentos["contents"])
        self.assertNotIn("r4", argumentos["contents"])

    @patch.object(criador_relatorio, "_validar_dados")
    def test_funciona_com_menos_de_tres_resumos(self, mock_validar):
        cliente = MagicMock()
        resposta = MagicMock()
        resposta.text = "Resumo curto"
        cliente.models.generate_content.return_value = resposta

        with patch.object(criador_relatorio, "cliente", cliente):
            resultado = criador_relatorio._gerar_resumo_inicial(
                {"Resumo": ["único"]}, "Alzheimer"
            )

        self.assertEqual(resultado, "Resumo curto")
        argumentos = cliente.models.generate_content.call_args.kwargs
        self.assertIn("único", argumentos["contents"])
        mock_validar.assert_called_once_with()

    @patch.object(criador_relatorio, "_validar_dados")
    def test_erro_de_validacao_impede_geracao(self, mock_validar):
        mock_validar.side_effect = ChaveInvalidaError("Modelo inválido")
        cliente = MagicMock()

        with patch.object(criador_relatorio, "cliente", cliente):
            with self.assertRaises(ChaveInvalidaError):
                criador_relatorio._gerar_resumo_inicial(
                    {"Resumo": ["r1"]}, "Alzheimer"
                )

        cliente.models.generate_content.assert_not_called()


class TestGerarRelatorio(unittest.TestCase):
    """Testes da função gerar_relatorio."""

    @patch.object(criador_relatorio, "Document")
    @patch.object(criador_relatorio, "_gerar_resumo_inicial")
    @patch.object(criador_relatorio, "procurar_resumos")
    def test_busca_resumos_e_salva_documento(
        self, mock_procurar, mock_gerar_resumo, mock_document
    ):
        resumos = {
            "Título": ["Título 1", "Título 2"],
            "Id": ["111", "222"],
            "Resumo": ["Resumo 1", "Resumo 2"],
        }
        mock_procurar.return_value = resumos
        mock_gerar_resumo.return_value = "Síntese"
        documento = MagicMock()
        mock_document.return_value = documento

        criador_relatorio.gerar_relatorio("Alzheimer", 2)

        mock_procurar.assert_called_once_with("Alzheimer", 2, imprimir=False)
        mock_gerar_resumo.assert_called_once_with(resumos, "Alzheimer")
        mock_document.assert_called_once_with()

        documento.add_heading.assert_any_call("Relatório sobre Alzheimer", 0)
        documento.add_heading.assert_any_call("Resumo Inicial", level=1)
        documento.add_paragraph.assert_any_call("Síntese")
        documento.add_heading.assert_any_call("Resumos", level=1)
        documento.add_heading.assert_any_call("Título 1", level=2)
        documento.add_paragraph.assert_any_call("Resumo 1")
        documento.add_heading.assert_any_call("Título 2", level=2)
        documento.add_paragraph.assert_any_call("Resumo 2")
        documento.save.assert_called_once_with("relatorio_Alzheimer.docx")

    @patch.object(criador_relatorio, "Document")
    @patch.object(criador_relatorio, "_gerar_resumo_inicial")
    @patch.object(criador_relatorio, "procurar_resumos")
    def test_erro_na_busca_impede_salvamento(
        self, mock_procurar, mock_gerar_resumo, mock_document
    ):
        mock_procurar.side_effect = RuntimeError("Falha na busca")
        documento = MagicMock()
        mock_document.return_value = documento

        with self.assertRaises(RuntimeError):
            criador_relatorio.gerar_relatorio("Alzheimer", 5)

        mock_gerar_resumo.assert_not_called()
        documento.save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
