#!/usr/bin/env python3
import os
from pathlib import Path
import tempfile
import unittest

from gemsModules.systemoperations.resources_api import Resource, Resources


class TestResourcesAPI(unittest.TestCase):

    def test_from_payload(self):
        res = Resource.from_payload("DManpa1-OH", role="Sequence", format="CondensedIUPAC")
        self.assertEqual(res.locationType, "Payload")
        self.assertEqual(res.resourceRole, "Sequence")
        self.assertEqual(res.resourceFormat, "CondensedIUPAC")
        self.assertEqual(res.payload, "DManpa1-OH")
        self.assertEqual(res.get_payload(), "DManpa1-OH")

    def test_from_file(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".pdb") as tmp:
            tmp.write("ATOM      1  N   ALA A   1      11.366  12.180  10.878  1.00 11.20           N\n")
            tmp_path = tmp.name

        try:
            res = Resource.from_file(tmp_path, role="Antibody", format="PDB")
            self.assertEqual(res.locationType, "filesystem-path-unix")
            self.assertEqual(res.resourceRole, "Antibody")
            self.assertEqual(res.resourceFormat, "PDB")
            self.assertTrue(res.get_payload().startswith("ATOM"))
            self.assertEqual(res.filename, Path(tmp_path).name)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_copy_to_and_copy_from(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            res_source = Resource.from_payload("HEADER TEST PDB DATA", role="Ligand", format="PDB", options={"filename": "ligand.pdb"})
            res_copied = res_source.copy_to(tmp_dir)

            self.assertEqual(res_copied.locationType, "filesystem-path-unix")
            dest_file = Path(tmp_dir) / "ligand.pdb"
            self.assertTrue(dest_file.is_file())
            self.assertEqual(dest_file.read_text(), "HEADER TEST PDB DATA")

            res_new = Resource()
            res_new.copy_from(res_copied)
            self.assertEqual(res_new.locationType, "filesystem-path-unix")
            self.assertEqual(res_new.payload, str(dest_file.resolve()))

    def test_resources_collection(self):
        resources = Resources()
        r1 = Resource.from_payload("DManpa1-OH", role="Sequence")
        r2 = Resource.from_payload("PDB DATA", role="Antibody")

        resources.append(r1)
        resources.append(r2)

        self.assertEqual(len(resources), 2)
        self.assertIsNotNone(resources.get_resource_by_role("Antibody"))
        self.assertEqual(resources.get_resource_by_role("Antibody").payload, "PDB DATA")


if __name__ == "__main__":
    unittest.main()
