import typer
import logging
from datetime import datetime
from pathlib import Path
from rich.progress import Progress
from rich.console import Console
from .validator import MutagenesisValidator
from .progress import progress_bar
from .mutagenex import mutate_multiple_residues

# Set up the progress bar and console
progress = progress_bar
console = Console()

app = typer.Typer()

@app.command()
def main(
    input_path: Path = typer.Argument(..., help="Directory containing the original PDB files."),
    output_path: Path = typer.Argument(..., help="Directory to save the mutated PDB files."),
    mutations: str = typer.Option(..., help="Comma-separated list of mutations or path to a mutation file."),
    log: bool = typer.Option(False, help="Enable logging to a file in the output directory.")
):
    """
    This command applies multiple mutations to all PDB files in the specified directory.
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

    # Step 5: Process the PDB files
    pdb_files = list(input_path.glob("*.pdb"))

    if not pdb_files:
        # Log the warning
        if log:
            logging.warning("WARNING: No PDB files found in the specified directory.")
        # Use rich to display a warning in yellow
        console.print("WARNING: No PDB files found in the specified directory.", style="bold yellow")
        return  # Exit without raising an exception

    # Always show the progress bar, even for a single file
    task = progress.add_task("[cyan]Mutating PDB files...", total=len(pdb_files))

    for pdb_file in pdb_files:
        # Apply mutations to the PDB file
        mutate_multiple_residues(pdb_file, mutations_list, output_path)

        # Log the mutation action
        if log:
            logging.info(f"Processed file: {pdb_file.name} with mutations: {mutations_list}")

        # Update progress bar for each file
        progress.update(task, advance=1)

    # Stop the progress bar
    progress.stop()

    # Success message
    console.print("Mutagenesis completed successfully!", style="bold green")
    if log:
        logging.info("Mutagenesis completed successfully.")
    # Final log message if needed
    if log:
        logging.info("Log file has been saved to: %s", log_file)


if __name__ == "__main__":
    app()
