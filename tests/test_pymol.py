import unittest
from unittest.mock import patch
from pathlib import Path
from rich.console import Console
from mutagenex.validator import MutagenesisValidator

class TestMutagenesisValidator(unittest.TestCase):

    @patch('mutagenex.validator.subprocess.run')
    def test_check_pymol_not_installed(self, mock_run):
        """
        Test the case where PyMOL is not installed.
        We mock subprocess.run to simulate a failure when checking PyMOL.
        """
        # Simula un errore che PyMOL non è trovato
        mock_run.side_effect = FileNotFoundError("PyMOL is not installed or not accessible.")
        
        # Inizializza il validatore
        validator = MutagenesisValidator()
        
        # Eseguiamo il controllo
        pymol_installed = validator.check_pymol_installed()
        
        # Verifica che la funzione restituisca False (PyMOL non è installato)
        self.assertFalse(pymol_installed)

    @patch('mutagenex.validator.subprocess.run')
    def test_check_pymol_installed(self, mock_run):
        """
        Test the case where PyMOL is installed.
        We mock subprocess.run to simulate PyMOL being available.
        """
        # Simula il successo del comando, indicando che PyMOL è installato
        mock_run.return_value = None  # Simula il successo del comando
        
        # Inizializza il validatore
        validator = MutagenesisValidator()
        
        # Eseguiamo il controllo
        pymol_installed = validator.check_pymol_installed()
        
        # Verifica che la funzione restituisca True (PyMOL è installato)
        self.assertTrue(pymol_installed)

if __name__ == '__main__':
    unittest.main()
