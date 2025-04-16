import re
from pathlib import Path
from typing import List
from rich.console import Console


class MutagenesisValidator:
    def __init__(self):
        """
        Initializes the MutagenesisValidator class with regex patterns for mutation validation.
        """
        # Create a console instance for printing colored messages
        self.console = Console()

        # Pattern for valid mutations: 'resno_chain_newresidue'
        self.mutation_pattern = re.compile(r'^\d+[A-Z]?_[A-Z]_[A-Z]{3}$') 
        
        # List of valid amino acids (3-letter code)
        self.valid_amino_acids = [
            'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 
            'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL'
        ]

    def validate_mutation_format(self, mutations: List[str]) -> bool:
        """
        Validates the format of each mutation in the provided list.
        :param mutations: List of mutations in the format 'chain_new_residue'.
        :return: True if all mutations are valid, False otherwise.
        """
        for mutation in mutations:
            # Split the mutation into chain and new residue
            parts = mutation.split('_')
            if len(parts) != 3:
                self.console.print(f"Error: Invalid mutation format '{mutation}', expected 'resno_chain_newresidue'.", style="bold red")
                return False
            
            resno, chain, new_residue = parts
            
            # Check if the chain is a single uppercase letter and the new residue is a 3-letter amino acid code
            if not (len(chain) == 1 and chain.isupper()):
                self.console.print(f"Error: Invalid chain '{chain}' in mutation '{mutation}'. Should be a single uppercase letter.", style="bold red")
                return False
            if not (len(new_residue) == 3 and new_residue.isupper()):
                self.console.print(f"Error: Invalid amino acid code '{new_residue}' in mutation '{mutation}'. Should be a 3-letter code.", style="bold red")
                return False
            if new_residue not in self.valid_amino_acids:
                self.console.print(f"Error: '{new_residue}' is not a valid amino acid code in mutation '{mutation}'.", style="bold red")
                return False
        
        return True

    def load_mutations(self, mutations_input: str) -> List[str]:
        """
        Loads mutations either from a string or from a file.
        :param mutations_input: A string of mutations or a path to a mutation file.
        :return: A list of mutations.
        """
        mutations = []
        mutations_path = Path(mutations_input)
        if mutations_path.is_file():
            mutations = self._load_mutations_from_file(mutations_path)
        elif mutations_path.suffix:
            self.console.print(f"Error: The path '{mutations_input}' is not a valid file.", style="bold red")
        else:
            mutations = self._load_mutations_from_string(mutations_input)
        
        return mutations

    def _load_mutations_from_file(self, file_path: Path) -> List[str]:
        """
        Helper method to load mutations from a file.
        :param file_path: Path to the file containing the mutations.
        :return: A list of mutations.
        """
        if not file_path.exists():
            self.console.print(f"Error: The file {file_path} does not exist.", style="bold red")
            return []
        
        with file_path.open('r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]

    def _load_mutations_from_string(self, mutations_input: str) -> List[str]:
        """
        Helper method to load mutations from a comma-separated string.
        :param mutations_input: A string of mutations separated by commas.
        :return: A list of mutations.
        """
        return mutations_input.split(',')

    def check_pymol_installed(self) -> bool:
        """
        Checks if PyMOL is installed as a Python package via pip, 
        and is accessible in the current environment.
        :return: True if PyMOL is installed as a Python module, False otherwise.
        """
        try:
            import pymol
            return True
        except ImportError:
            self.console.print("Error: PyMOL is not installed as a Python package or not accessible in the environment.", style="bold red")
            return False
