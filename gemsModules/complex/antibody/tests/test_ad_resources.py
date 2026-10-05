#!/usr/bin/env python3
from pathlib import Path
import tempfile
import unittest

from gemsModules.systemoperations.resources_api import Resource, Resources


class TestAntibodyDockingResources(unittest.TestCase):

    def test_ad_input_resources(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".pdb") as tmp_ab:
            tmp_ab.write("HEADER ANTIBODY PDB\nATOM 1 N ALA A 1 0.0 0.0 0.0\n")
            ab_path = tmp_ab.name

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".pdb") as tmp_lig:
            tmp_lig.write("HEADER LIGAND PDB\nATOM 1 N GLY B 1 1.0 1.0 1.0\n")
            lig_path = tmp_lig.name

        try:
            ab_res = Resource.from_file(ab_path, role="Antibody", format="chemical/pdb")
            lig_res = Resource.from_file(lig_path, role="Ligand", format="chemical/pdb")

            resources = Resources()
            resources.append(ab_res)
            resources.append(lig_res)

            self.assertEqual(len(resources), 2)
            self.assertEqual(resources.get_resource_by_role("Antibody").payload, str(Path(ab_path).resolve()))
            self.assertEqual(resources.get_resource_by_role("Ligand").payload, str(Path(lig_path).resolve()))

            self.assertTrue(resources.get_resource_by_role("Antibody").get_payload().startswith("HEADER ANTIBODY"))
            self.assertTrue(resources.get_resource_by_role("Ligand").get_payload().startswith("HEADER LIGAND"))
        finally:
            import os
            if os.path.exists(ab_path):
                os.remove(ab_path)
            if os.path.exists(lig_path):
                os.remove(lig_path)


if __name__ == "__main__":
    unittest.main()
