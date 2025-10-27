"""import unittest
from unittest.mock import patch, call
import io
import sys
import os

# Adiciona o diretório 'src' ao path para permitir a importação dos módulos do projeto
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

from src import Headers

class TestHeaders(unittest.TestCase):

    @patch('Headers.clear_menu')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_menu_output(self, mock_stdout, mock_clear_menu):
        """
        #Testa se a função main_menu imprime o menu esperado e chama clear_menu.
        #"""
        # Chama a função que queremos testar
        #Headers.main_menu()

        # 1. Verifica se a função para limpar o menu foi chamada uma vez
        #mock_clear_menu.assert_called_once()

        # 2. Verifica se a saída impressa no console é exatamente a esperada
        #expected_output = (
        #    f"{'='*20}\n"
         #   "1 - Novo usuario\n"
          #  "2 - Login\n"
           # "3 - Exibir notas\n"
            #"0 - Finalizar programa\n"
            #f"{'='*20}\n"
        #)
        #self.assertEqual(mock_stdout.getvalue(), expected_output)

#if __name__ == '__main__':
#    unittest.main(verbosity=2)
from src import Headers
subject_selected = Headers.subject_names()
print(subject_selected)
