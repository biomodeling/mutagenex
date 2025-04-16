# mutagenex
[![Version](figures/version.svg)](https://github.com/biomodeling/mutagenex)
![Python Version](figures/python.svg)
[![License: GPL v3](figures/license.svg)](https://github.com/biomodeling/mutagenex/blob/master/LICENSE.md)

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

The program will apply these mutations to all PDB files found in the input directory and save the mutated files to the output directory.

**Arguments**

* `input_path`: Directory containing the original PDB files or a single PDB file.
* `output_path`: Directory to save the mutated PDB files.
* `--mutations`: Comma-separated list of mutations or path to a mutation file.
* `--log`: Enable logging to a file in the output directory.
* `--help`


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

### As CLI

#### 1. Build the Package

Use the following command to create the distribution files:

```bash
python -m build
```

This will create the distribution files in the `dist/` directory, such as `.tar.gz` or `.whl` files.

#### 2. Install the Package

Once the build is successful, install the package in the same pymol enviroment using `pip`:

```bash
pip install dist/mutagenex-0.1.0.tar.gz
```

#### 3. Create a Wrap Script (optional)

If you installed pymol and mutagenex in a virtual environment, a wrap script allows you to execute the package from anywhere without needing to manually activate the virtual environment each time.

Create a script called `mutagenex` (or any name you prefer) in the `~/.local/bin/` directory (or another directory included in your `PATH`).

Here’s a simple wrap script:

```bash
#!/bin/bash
# This is the wrap for your Python script

# Activate the virtual environment if necessary
source /path/to/your/venv/bin/activate

# Run the Python module
mutagenex "$@"
```

Ensure the wrap script is executable:

```bash
chmod +x ~/.local/bin/mutagenex
```

Now you can call `mutagenex` from anywhere, and it will run the package as expected.


#### Verifying the Setup  
Once the wrap is set up, you can verify it by running:

```bash
mutagenex --help
```

If everything is set up correctly, this will display the help message from your `mutagenex.cli` module.



## Run test
- ```python -m unittest discover -s tests -p "test_pymol.py"```
- ```python -m unittest discover -s tests -p "test_validator.py"```
