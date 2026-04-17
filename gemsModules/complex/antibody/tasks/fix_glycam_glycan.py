def execute(glycan_path: str) -> bool:
    """ Checks if there is an END card at the end of a pdb file. If not, adds one.

        Returns:
            bool: True if an END card was added, False otherwise
    """
    with open(glycan_path, "r") as f:
        lines = f.readlines()
    
    if not lines[-1].startswith("END"):
        with open(glycan_path, "a") as f:
            f.write("END\n")
            return True
    
    return False
