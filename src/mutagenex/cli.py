import typer
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
):
    """
    This command applies multiple mutations to all PDB files in the specified directory.
    """

    # Step 1: Initialize the mutation validator
    validator = MutagenesisValidator()

    # Step 2: Check if PyMOL is installed
    if not validator.check_pymol_installed():
        # Use rich to display a red error message
        console.print("ERROR: PyMOL is not installed or not accessible. Please install PyMOL.", style="bold red")
        return  # Exit without raising an exception

    # Step 3: Load mutations from the provided input (string or file path)
    mutations_list = validator.load_mutations(mutations)

    # Step 4: Validate the mutation format
    if not validator.validate_mutation_format(mutations_list):
        # Use rich to display a red error message
        console.print("ERROR: Invalid mutation format detected. Please correct the mutations.", style="bold red")
        return  # Exit without raising an exception

    # Step 5: Process the PDB files
    pdb_files = list(input_path.glob("*.pdb"))

    if not pdb_files:
        # Use rich to display a warning in yellow
        console.print("WARNING: No PDB files found in the specified directory.", style="bold yellow")
        return  # Exit without raising an exception

    # Always show the progress bar, even for a single file
    task = progress.add_task("[cyan]Mutating PDB files...", total=len(pdb_files))

    for pdb_file in pdb_files:
        # Apply mutations to the PDB file
        mutate_multiple_residues(pdb_file, mutations_list, output_path)

        # Update progress bar for each file
        progress.update(task, advance=1)

    # Stop the progress bar
    progress.stop()

    # Success message
    console.print("Mutagenesis completed successfully!", style="bold green")


if __name__ == "__main__":
    app()
