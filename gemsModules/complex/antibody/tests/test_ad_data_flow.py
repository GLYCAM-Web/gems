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

        self.orig_aad2_docker_home = os.environ.get("AAD2_DOCKER_HOME")
        self.mock_aad2_home = os.path.join(self.temp_dir, "mock_aad2")
        os.makedirs(self.mock_aad2_home, exist_ok=True)
        os.environ["AAD2_DOCKER_HOME"] = self.mock_aad2_home

    def tearDown(self):
        if self.orig_aad2_docker_home is not None:
            os.environ["AAD2_DOCKER_HOME"] = self.orig_aad2_docker_home
        else:
            os.environ.pop("AAD2_DOCKER_HOME", None)
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

        with open(os.path.join(self.project_dir, "gwconfig"), "r") as f:
            gw_content = f.read()
            self.assertIn("PARTITION=", gw_content)
            self.assertIn("DOCKING_REPLICA_BATCH_CPUS=", gw_content)

        # Subsequent run without resources should preserve existing filenames in ad2config
        pm_inputs_no_res = ProjectManagement_Inputs(
            pUUID=self.puuid,
            projectDir=self.project_dir,
            resources=Resources(__root__=[])
        )
        execute_pm(pm_inputs_no_res)
        with open(os.path.join(self.project_dir, "ad2config"), "r") as f:
            content_after = f.read()
            self.assertIn("Antibody_File_Name=\"test_ab.pdb\"", content_after)
            self.assertIn("Glycan_File_Name=\"test_lig.pdb\"", content_after)

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

    def test_project_management_missing_path_returns_notice(self):
        from unittest.mock import patch
        from gemsModules.complex.antibody.services.ProjectManagement.server import Serve

        pm_inputs = ProjectManagement_Inputs(
            pUUID=self.puuid,
            projectDir=os.path.join(self.temp_dir, "missing_path_proj"),
            resources=Resources(__root__=[self.ab_resource, self.lig_resource])
        )

        with patch.dict(os.environ, {}, clear=True), \
             patch("gemsModules.complex.antibody.services.ProjectManagement.logic.resolve_aad2_configuration", return_value=None):
            # 1. Test logic execution directly
            outputs = execute_pm(pm_inputs)
            self.assertIsNotNone(outputs.notices)
            self.assertIsNotNone(outputs.notices.__root__)
            notice = next((n for n in outputs.notices.__root__ if n.Brief == "PathNotConfigured"), None)
            self.assertIsNotNone(notice, "Expected PathNotConfigured notice in outputs")
            self.assertEqual(notice.Type, "Error")
            self.assertEqual(notice.Code, "404")
            self.assertIn("not configured", notice.Message)

            # 2. Test through Serve
            pm_req = ProjectManagement_Request(inputs=pm_inputs)
            resp = Serve(pm_req)
            self.assertIsNotNone(resp.notices)
            self.assertIsNotNone(resp.notices.__root__)
            resp_notice = next((n for n in resp.notices.__root__ if n.Brief == "PathNotConfigured"), None)
            self.assertIsNotNone(resp_notice, "Expected PathNotConfigured notice in response")
            self.assertEqual(resp_notice.Type, "Error")

    def test_project_management_env_override(self):
        from unittest.mock import patch
        custom_env_dir = os.path.join(self.temp_dir, "custom_env_aad2")
        env_proj_dir = os.path.join(self.temp_dir, "env_proj")

        pm_inputs = ProjectManagement_Inputs(
            pUUID=self.puuid,
            projectDir=env_proj_dir,
            resources=Resources(__root__=[self.ab_resource, self.lig_resource])
        )

        with patch.dict(os.environ, {"AAD2_DOCKER_HOME": custom_env_dir}):
            outputs = execute_pm(pm_inputs)
            self.assertTrue(os.path.exists(os.path.join(env_proj_dir, "ad2config")))
            with open(os.path.join(env_proj_dir, "ad2config"), "r") as f:
                content = f.read()
                self.assertTrue(
                    f'AAD2_DOCKER_HOME="{custom_env_dir}"' in content or
                    f"AAD2_DOCKER_HOME='{custom_env_dir}'" in content
                )
                self.assertTrue(
                    f'AAD2_CLI_BIN_PATH="{custom_env_dir}/image/AAD2/bin"' in content or
                    f"AAD2_CLI_BIN_PATH='{custom_env_dir}/image/AAD2/bin'" in content
                )

    def test_response_manager_aggregates_service_notices(self):
        from gemsModules.common.action_associated_objects import AAOP_Tree_Pair, AAOP_Tree, Annotated_List
        from gemsModules.complex.antibody.services.ProjectManagement.api import ProjectManagement_Response
        from gemsModules.complex.antibody.services.response_manager import Antibody_Response_Manager

        pm_req = ProjectManagement_Request(
            inputs=ProjectManagement_Inputs(pUUID=self.puuid, projectDir=self.project_dir)
        )
        pm_resp = ProjectManagement_Response()
        pm_resp.notices.addNotice(
            Brief="TestWarning",
            Scope="Service",
            Messenger="AD",
            Type="Warning",
            Code="300",
            Message="Test notice message",
        )

        req_pkg = AAOP(AAO_Type="ProjectManagement", The_AAO=pm_req, Dictionary_Name="PM")
        resp_pkg = AAOP(AAO_Type="ProjectManagement", The_AAO=pm_resp, Dictionary_Name="PM")

        tree_pair = AAOP_Tree_Pair(
            input_tree=AAOP_Tree(packages=Annotated_List([req_pkg])),
            output_tree=AAOP_Tree(packages=Annotated_List([resp_pkg]))
        )

        rm = Antibody_Response_Manager(aaop_tree_pair=tree_pair)
        resp_entity = rm.process()
        self.assertIsNotNone(resp_entity.notices)
        self.assertIsNotNone(resp_entity.notices.__root__)
        aggregated = next((n for n in resp_entity.notices.__root__ if n.Brief == "TestWarning"), None)
        self.assertIsNotNone(aggregated)
        self.assertEqual(aggregated.Message, "Test notice message")

    def test_build_logic_accepts_none_or_partial_options(self):
        from unittest.mock import patch, MagicMock
        from gemsModules.complex.antibody.services.Build.logic import execute as execute_build
        from gemsModules.complex.antibody.services.Build.api import Build_Inputs, Build_Options

        pm_inputs = ProjectManagement_Inputs(
            pUUID=self.puuid,
            projectDir=self.project_dir,
            resources=Resources(__root__=[self.ab_resource, self.lig_resource])
        )
        execute_pm(pm_inputs)

        build_inputs = Build_Inputs(pUUID=self.puuid, projectDir=self.project_dir)

        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch("gemsModules.complex.antibody.services.Build.logic.run_ad_build.execute", return_value=mock_result):
            # 1. Test with options=None
            outputs, notices = execute_build(build_inputs, options=None)
            self.assertTrue(any(n.Brief == "Build Successful" for n in notices.__root__))

            # 2. Test with Build_Options instance
            outputs, notices = execute_build(build_inputs, options=Build_Options(count=3, flexibility="rigid"))
            self.assertTrue(any(n.Brief == "Build Successful" for n in notices.__root__))

    def test_interface_evaluation_followed_by_build(self):
        """
        End-to-end interface test:
        1. Submits evaluation request JSON through Antibody_Json_String_Manager.
           Verifies ProjectManagement creates ad2config, gwconfig, vcconfig,
           and Evaluate returns success without running actual AAD2 evaluate execution.
        2. Submits build request JSON using the assigned pUUID and options.
           Verifies Build updates options in ad2config and returns success
           without running actual AAD2 build execution.
        """
        import json
        from unittest.mock import patch, MagicMock
        from gemsModules.complex.antibody.json_string_manager import Antibody_Json_String_Manager

        # Step 1: Evaluation request matching website / GEMS schema
        eval_request_json = {
            "entity": {
                "type": "AntibodyDocking",
                "services": {
                    "evaluation_of_pdb": {
                        "type": "Evaluate",
                        "inputs": {
                            "resources": [
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "resourceRole": "Antibody",
                                    "payload": self.ab_file,
                                },
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "resourceRole": "Ligand",
                                    "payload": self.lig_file,
                                },
                            ],
                        },
                    }
                },
            },
            "prettyPrint": True,
        }

        mock_eval_res = MagicMock(returncode=0, stderr="")
        mock_build_res = MagicMock(returncode=0, stderr="")

        with patch("gemsModules.complex.antibody.tasks.run_ad_evaluate.execute", return_value=mock_eval_res), \
             patch("gemsModules.complex.antibody.tasks.run_detect_sugars.execute", return_value="/tmp/fake_ring.txt"):
            eval_manager = Antibody_Json_String_Manager()
            err = eval_manager.process(incoming_string=json.dumps(eval_request_json))
            self.assertIsNone(err, f"Evaluation processing failed: {err}")

            eval_resp_str = eval_manager.transaction.get_outgoing_string()
            eval_resp = json.loads(eval_resp_str)
            self.assertEqual(eval_resp["entity"]["type"], "AntibodyDocking")

            proj_info = eval_resp.get("project", {})
            assigned_puuid = proj_info.get("pUUID")
            self.assertIsNotNone(assigned_puuid)
            project_dir = proj_info.get("project_dir")
            self.assertIsNotNone(project_dir)
            self.assertTrue(os.path.isdir(project_dir))

            # Verify that ProjectManagement created all required config files
            self.assertTrue(os.path.exists(os.path.join(project_dir, "ad2config")))
            self.assertTrue(os.path.exists(os.path.join(project_dir, "gwconfig")))
            self.assertTrue(os.path.exists(os.path.join(project_dir, "vcconfig")))

        # Step 2: Build request following evaluation
        build_request_json = {
            "entity": {
                "type": "AntibodyDocking",
                "services": {
                    "build": {
                        "type": "Build",
                        "inputs": {
                            "pUUID": assigned_puuid,
                            "resources": [
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "resourceRole": "Antibody",
                                    "payload": self.ab_file,
                                },
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "resourceRole": "Ligand",
                                    "payload": self.lig_file,
                                },
                            ],
                        },
                        "options": {
                            "Glycan_Flexibility": "Rigid",
                            "Number_of_Replicas": 5,
                        },
                    }
                },
            },
            "prettyPrint": True,
        }

        with patch("gemsModules.complex.antibody.tasks.run_ad_build.execute", return_value=mock_build_res):
            build_manager = Antibody_Json_String_Manager()
            berr = build_manager.process(incoming_string=json.dumps(build_request_json))
            self.assertIsNone(berr, f"Build processing failed: {berr}")

            build_resp_str = build_manager.transaction.get_outgoing_string()
            build_resp = json.loads(build_resp_str)
            self.assertEqual(build_resp["entity"]["type"], "AntibodyDocking")

            # Verify that options in ad2config were updated
            with open(os.path.join(project_dir, "ad2config"), "r") as f:
                ad2_content = f.read()
                self.assertTrue(
                    'Glycan_Flexibility="Rigid"' in ad2_content or "Glycan_Flexibility='Rigid'" in ad2_content
                )
                self.assertTrue(
                    'Number_of_Replicas="5"' in ad2_content or "Number_of_Replicas='5'" in ad2_content
                )


if __name__ == "__main__":
    unittest.main()
