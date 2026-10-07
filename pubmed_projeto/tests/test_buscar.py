"""
Ambiente de testes do módulo buscar
"""

import unittest
from pubmed_projeto.src.buscar import _validar_argumentos, _buscar_conteudo, _buscar_ids, _extrair_pubmedid, _extrair_resumo, _extrair_resumo_completo, _extrair_titulo, procurar_resumos

class TestValidarArgumentos(unittest.TestCase):
    """
    """
    def test_tipos_ids_diferente_de_int(self):
        with self.assertRaises(TypeError):
            _validar_argumentos("Alzheimer", numero_de_ids="5")