import typer
import logging
from datetime import datetime
from pathlib import Path
from rich.console import Console
from .validator import MutagenesisValidator
from .utils import progress_bar
from .mutagenex import mutate_multiple_residues


console = Console()
app = typer.Typer(rich_markup_mode="markdown")

@app.command()
def main(
    input_path: Path = typer.Argument(..., help="Directory containing the original PDB files or a single PDB file."),
    output_path: Path = typer.Argument(..., help="Directory to save the mutated PDB files."),
    mutations: str = typer.Option(..., help="Comma-separated list of mutations or path to a mutation file."),
    log: bool = typer.Option(False, help="Enable logging to a file in the output directory.")
):
    """
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
    
    1. As a comma-separated list of mutations (a single string), e.g.: ```58_A_PRO,110A_H_ALA,2_B_LYS```
    
    2. As a `.txt` file where each line represents a mutation, e.g.:

    ```
    
    58_A_PRO
    
    110A_H_ALA
    
    2_B_LYS
    
    ```
    

    The program will apply these mutations to all PDB files found in the input directory and save the 
    mutated files to the output directory.
    """
    # Step 1: Initialize the mutation validator
    validator = MutagenesisValidator()

    # Set up the log file if needed
    log_file = None
    if log:
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
        log_file = output_path / f"mutagenex_{timestamp}.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Log started for mutagenesis process.")

    # Step 2: Check if PyMOL is installed
    if not validator.check_pymol_installed():
        # Log the error
        if log:
            logging.error("ERROR: PyMOL is not installed or not accessible.")
        # Use rich to display a red error message
        console.print("ERROR: PyMOL is not installed or not accessible. Please install PyMOL.", style="bold red")
        return  # Exit without raising an exception

    # Step 3: Load mutations from the provided input (string or file path)
    mutations_list = validator.load_mutations(mutations)

    # Log the loaded mutations
    if log:
        logging.info(f"Loaded mutations: {mutations_list}")

    # Step 4: Validate the mutation format
    if not validator.validate_mutation_format(mutations_list):
        # Log the error
        if log:
            logging.error("ERROR: Invalid mutation format detected.")
        # Use rich to display a red error message
        console.print("ERROR: Invalid mutation format detected. Please correct the mutations.", style="bold red")
        return  # Exit without raising an exception

    # Step 5: Handle input path (single file or directory)
    if input_path.is_dir():
        # If it's a directory, find all PDB files
        pdb_files = list(input_path.glob("*.pdb"))
    elif input_path.is_file() and input_path.suffix == ".pdb":
        # If it's a single PDB file
        pdb_files = [input_path]
    else:
        # If neither a valid directory nor a valid file
        console.print("ERROR: Invalid input path. Please provide a valid directory or a single PDB file.", style="bold red")
        return

    if not pdb_files:
        # Log the warning
        if log:
            logging.warning("WARNING: No PDB files found in the specified directory.")
        # Use rich to display a warning in yellow
        console.print("WARNING: No PDB files found in the specified directory.", style="bold yellow")
        return  # Exit without raising an exception

    warning_list = []

    with progress_bar as progress:
        task = progress.add_task("[cyan]Processing...", total=len(pdb_files))

        for pdb_file in pdb_files:
            # Apply mutations to the PDB file
            mutate_multiple_residues(pdb_file, mutations_list, output_path, log, warning_list)

            # Log the mutation action
            if log:
                logging.info(f"Processed file: {pdb_file.name} with mutations: {mutations_list}")

            # Update progress bar for each file
            progress.update(task, advance=1)

    if warning_list:
        for warning in warning_list:
            if log:
                logging.warning(warning)
        if log:
            console.print("WARNING: Some mutations could not be applied. Check the log for details.", style="bold yellow")
        else:
            console.print("WARNING: Some mutations could not be applied. Run again with --log for more details.", style="bold yellow")

    # Success message
    console.print("Mutagenesis completed successfully!", style="bold green")
    if log:
        logging.info("Mutagenesis completed successfully.")
        logging.info("Log file has been saved to: %s", log_file)


if __name__ == "__main__":
    app()

