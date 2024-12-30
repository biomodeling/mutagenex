# mutagenex

Make single or multiple mutations from command line with pymol.

Each mutation must be represented by a string consisting of three elements,
separated by an underscore (_):
- Residue number to be mutated
- Chain of the residue to be mutated (single uppercase letter)
- New residue (three-letter code)

Example: '58_A_PRO' means to mutate residue 58 of chain A to proline.

The residue number can include letters (e.g. 110A) and any valid selection that PyMOL can identify.
The chain identifier must be a single uppercase letter (e.g., 'A', 'B', 'C').

Mutations can be provided in two formats:
1. As a comma-separated list of mutations (a single string), e.g.: `58_A_PRO,110A_H_ALA,2_B_LYS`
2. As a `.txt` file where each line represents a mutation, e.g.:
    ```
    58_A_PRO
    110A_H_ALA
    2_B_LYS
    ```

The program will apply these mutations to all PDB files found in the input directory and save the 
mutated files to the output directory.

## Run script

### As a module
**NOTE**: `pymol` must be installed as python package

1. string:
    ```
    python -m mutagenex.cli ./tests/data/input/ ./tests/data/output/ --mutations="108_B_ASP,109_B_PRO,110_B_VAL,111_B_VAL,112A_B_TYR,113_B_GLY,214_B_TRP"
    ```
2. file
    ```
    python -m mutagenex.cli ./tests/data/input/ ./tests/data/output/ --mutations=./tests/data/mutations.txt --log
    ```

### wrap


## Run test
- ```python -m unittest discover -s tests -p "test_pymol.py"```
- ```python -m unittest discover -s tests -p "test_validator.py"```
