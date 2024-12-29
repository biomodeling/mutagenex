import unittest
from pathlib import Path
from mutagenex.validator import MutagenesisValidator


class TestMutagenesisValidator(unittest.TestCase):

    def setUp(self):
        # Crea un'istanza di MutagenesisValidator
        self.validator = MutagenesisValidator()

    def test_valid_mutations(self):
        # Mutazioni valide nel formato 'residue_number_chain_new_residue'
        mutations = "112A_A_PRO,65A_A_ALA,110B_B_LYS"
        result = self.validator.validate_mutation_format(mutations.split(','))
        self.assertTrue(result)

    def test_invalid_format_mutations(self):
        # Mutazioni con formato errato
        mutations = [
            "59A_PRO",  # Manca l'underscore
            "65_AAAA",  # Il codice dell'amminoacido è troppo lungo
            "110_B_LYSX",  # Il codice dell'amminoacido è errato
        ]
        result = self.validator.validate_mutation_format(mutations)
        self.assertFalse(result)

    def test_invalid_chain(self):
        # Mutazione con catena non valida
        mutations = "112A_a_PRO"  # La lettera della catena dovrebbe essere maiuscola
        result = self.validator.validate_mutation_format([mutations])
        self.assertFalse(result)

    def test_invalid_amino_acid(self):
        # Mutazione con un amminoacido non valido
        mutations = "112_A_INVALID"  # 'INVALID' non è un amminoacido valido
        result = self.validator.validate_mutation_format([mutations])
        self.assertFalse(result)

    def test_load_mutations_from_string(self):
        # Test per caricare mutazioni da una stringa separata da virgole
        mutations_input = "112A_A_PRO,65A_A_ALA,110B_B_LYS"
        mutations = self.validator.load_mutations(mutations_input)
        self.assertEqual(mutations, ["112A_A_PRO", "65A_A_ALA", "110B_B_LYS"])

    def test_load_mutations_from_file(self):
        # Creazione di un file temporaneo di test
        file_path = Path("tests/data/mutations.txt")
        with open(file_path, "w") as file:
            file.write("112A_A_PRO\n65A_A_ALA\n110B_B_LYS\n")
        
        mutations = self.validator.load_mutations(file_path)
        if file_path.exists():
            file_path.unlink()
        self.assertEqual(mutations, ["112A_A_PRO", "65A_A_ALA", "110B_B_LYS"])

    def test_load_mutations_file_not_found(self):
        # empty list if file doesn't exist
        mutations = self.validator.load_mutations("non_existing_file.txt")
        self.assertEqual(mutations, [])

    def test_invalid_file_format(self):
        file_path = Path("tests/data/invalid_mutations.txt")
        
        with open(file_path, "w") as file:
            file.write("112A_A_PRO\ninvalid_line\n65A_A_ALA\n110B_B_LYS\n")
        
        mutations = self.validator.load_mutations(file_path)
        if file_path.exists():
            file_path.unlink()
        result = self.validator.validate_mutation_format(mutations)        
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
