from pathlib import Path
import logging


def mutate_multiple_residues(pdb_file: Path, mutations: list, output_directory: Path):
    """
    Applies mutations to a single PDB file.
    :param pdb_file: The PDB file to be mutated.
    :param mutations: A list of mutations in the format 'residue_number_chain_new_residue'.
    :param output_directory: The directory where the mutated PDB files will be saved.
    """
    # Load the PDB file and start the mutagenesis wizard in PyMOL
    cmd.load(str(pdb_file))
    cmd.wizard("mutagenesis") 
    
    # Apply each mutation
    for mutation in mutations:
        residue_position, chain_id, new_residue = mutation.split('_')

        # Select residue to mutate
        selection = f"{chain_id}/{residue_position}/"
        cmd.get_wizard().do_select(selection)

        # Check if the selection is valid (if there are atoms selected)
        if cmd.count_atoms(selection) == 0:
            # Log the error if the mutation is not valid (selection is empty)
            if log:
                logging.error(f"Mutation {mutation} could not be applied. Residue {residue_position} in chain {chain_id} not found in {pdb_file.name}.")
            continue  # Skip this mutation and move to the next one

        cmd.get_wizard().set_mode(new_residue)
        cmd.get_wizard().apply()

    # Save the mutated PDB file
    output_filename = output_directory / pdb_file.name
    cmd.set_wizard()  # End the mutagenesis wizard
    cmd.save(str(output_filename))  # Save the mutated PDB file
    cmd.delete('all')  # Clear the memory in PyMOL
