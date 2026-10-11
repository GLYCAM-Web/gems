#!/usr/bin/env python3
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.complex.antibody.services.Evaluate.api import Evaluate_Request, Evaluate_Inputs
from gemsModules.complex.antibody.services.Build.api import Build_Request, Build_Inputs
from gemsModules.complex.antibody.services.ProjectManagement.api import ProjectManagement_Request, ProjectManagement_Inputs
from gemsModules.complex.antibody.services.ProjectManagement.logic import execute as execute_pm
from gemsModules.complex.antibody.services.request_data_filler import Antibody_Request_Data_Filler
from gemsModules.complex.antibody.tasks import update_build_options
from gemsModules.complex.antibody.main_api import Antibody_Transaction
from gemsModules.complex.antibody.main_api_project import AntibodyProject


class TestAntibodyDataFlow(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = os.path.join(self.temp_dir, "test_proj_12345")
        self.puuid = "12345-abcde-67890"

        # Create dummy PDB files
        self.ab_file = os.path.join(self.temp_dir, "test_ab.pdb")
        with open(self.ab_file, "w") as f:
            f.write("HEADER TEST ANTIBODY\nATOM 1 N ALA A 1 0.0 0.0 0.0\n")

        self.lig_file = os.path.join(self.temp_dir, "test_lig.pdb")
        with open(self.lig_file, "w") as f:
            f.write("HEADER TEST LIGAND\nATOM 1 N GLY B 1 1.0 1.0 1.0\n")

        self.ab_resource = Resource(
            locationType="filesystem-path-unix",
            resourceRole="Antibody",
            resourceFormat="chemical/pdb",
            payload=self.ab_file,
            options={"filename": "test_ab.pdb"},
        )
        self.lig_resource = Resource(
            locationType="filesystem-path-unix",
            resourceRole="Ligand",
            resourceFormat="chemical/pdb",
            payload=self.lig_file,
            options={"filename": "test_lig.pdb"},
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_evaluate_and_build_inputs_have_project_dir(self):
        eval_inputs = Evaluate_Inputs(pUUID=self.puuid, projectDir=self.project_dir)
        self.assertEqual(eval_inputs.projectDir, self.project_dir)
        self.assertEqual(eval_inputs.pUUID, self.puuid)

        build_inputs = Build_Inputs(pUUID=self.puuid, projectDir=self.project_dir)
        self.assertEqual(build_inputs.projectDir, self.project_dir)
        self.assertEqual(build_inputs.pUUID, self.puuid)

    def test_project_management_logic_creates_configs(self):
        pm_inputs = ProjectManagement_Inputs(
            pUUID=self.puuid,
            projectDir=self.project_dir,
            resources=Resources(__root__=[self.ab_resource, self.lig_resource])
        )
        outputs = execute_pm(pm_inputs)
        self.assertTrue(os.path.isdir(self.project_dir))
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, "ad2config")))
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, "gwconfig")))
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, "vcconfig")))

        with open(os.path.join(self.project_dir, "ad2config"), "r") as f:
            content = f.read()
            self.assertIn("Antibody_File_Name=\"test_ab.pdb\"", content)
            self.assertIn("Glycan_File_Name=\"test_lig.pdb\"", content)

    def test_update_build_options_supports_aliases(self):
        pm_inputs = ProjectManagement_Inputs(
            pUUID=self.puuid,
            projectDir=self.project_dir,
            resources=Resources(__root__=[self.ab_resource, self.lig_resource])
        )
        execute_pm(pm_inputs)

        # Test with user-friendly options: "flexibility" and "count"
        options = {"flexibility": "rigid", "count": 10}
        update_build_options.execute(options, self.project_dir)

        with open(os.path.join(self.project_dir, "ad2config"), "r") as f:
            content = f.read()
            self.assertTrue("Glycan_Flexibility=\"Rigid\"" in content or "Glycan_Flexibility='Rigid'" in content)
            self.assertTrue("Number_of_Replicas=\"10\"" in content or "Number_of_Replicas='10'" in content)

    def test_request_data_filler_injects_project_dir(self):
        from gemsModules.complex.antibody.main_api import Antibody_Entity
        transaction = Antibody_Transaction()
        transaction.inputs = transaction.get_API_type()(entity=Antibody_Entity(type="AntibodyDocking"))
        proj = AntibodyProject()
        proj.pUUID = self.puuid
        proj.project_dir = self.project_dir
        transaction.inputs.project = proj

        eval_aaop = AAOP(
            AAO_Type="Evaluate",
            The_AAO=Evaluate_Request(),
            Dictionary_Name="Evaluate",
        )
        build_aaop = AAOP(
            AAO_Type="Build",
            The_AAO=Build_Request(),
            Dictionary_Name="Build",
        )
        pm_aaop = AAOP(
            AAO_Type="ProjectManagement",
            The_AAO=ProjectManagement_Request(),
            Dictionary_Name="PM",
        )

        filler = Antibody_Request_Data_Filler(
            aaop_list=[pm_aaop, eval_aaop, build_aaop],
            transaction=transaction,
            response_project=proj,
        )

        filled = filler.process(transaction)
        self.assertEqual(eval_aaop.The_AAO.inputs.projectDir, self.project_dir)
        self.assertEqual(build_aaop.The_AAO.inputs.projectDir, self.project_dir)
        self.assertEqual(eval_aaop.The_AAO.inputs.pUUID, self.puuid)
        self.assertEqual(build_aaop.The_AAO.inputs.pUUID, self.puuid)


if __name__ == "__main__":
    unittest.main()
