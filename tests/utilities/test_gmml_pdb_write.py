#!/usr/bin/env python3

import os
import gmml


if __name__ == "__main__":
    TEST_FILE = "/programs/gems/tests/inputs/016.AmberMDPrep.4mbzEdit.pdb"
    OUT_FILE = "/programs/gems/tests/preprocessed.016.AmberMDPrep.4mbzEdit.pdb"

    f = gmml.cds_PdbFile(TEST_FILE)
    f.Write(OUT_FILE)

    if not os.path.exists(OUT_FILE):
        raise IOError("PDB File not written")

    print("PDB File written")
    os.remove(OUT_FILE)
