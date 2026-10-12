import io
import json
import os
import sys
import tempfile
import unittest

# Configure paths
sys.path.insert(0, "/programs/gems")

from gemsModules.configuration.main_api import InstanceConfig, session_instance_config, set_session_instance_config
from gemsModules.logging.loggingConfig import is_stderr_suppressed
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.complex.antibody.receive import receive

ic_data = {
  "date": "2026-10-03T22:55:21.348972",
  "hosts": [
    {
      "is_localhost": "True",
      "name": "Thoreau",
      "address": "172.16.4.2",
      "port": "42059",
      "execution_environments": [
        "Swarm",
        "Batch",
        "Docker",
        "NodeDocker",
        "Standalone",
        "Website"
      ],
      "website_environments": [
        "DevEnv"
      ],
      "entities_available": [
        "AD"
      ],
      "scheduler": "slurm",
      "batch_computing_resources": [
        {
          "partition": "wCPU",
          "supported_entities": [
            "AD"
          ],
          "max_nodes_per_job": "1",
          "max_cores_per_node": "28",
          "max_threads_per_node": "56",
          "max_gpus_per_node": "0",
          "max_cpus_per_gpu": "0",
          "max_time_limit": "600"
        }
      ],
      "resource_specific_information": {
        "use_gres_for_gpus": "True",
        "cpu_hardware_equivalent": "core",
        "aad2_configuration": {
          "aad2_docker_home": "/programs/website/deployment/development-environment/AAD2_Docker",
          "aad2_image_file_path": "/programs/website/COMMON/aad2/image_files",
          "image": "antibody-docking:2025-03-31-00-22-blf",
          "vmd_home": "/programs/website/bin",
          "vmd_lib": "/programs/website/lib/vmd"
        }
      }
    }
  ],
  "filesystem_paths": {
    "AD": "/tmp/testAAD2/remote/ad"
  },
  "secure_inputs_paths": {
    "AD": "/tmp/testAAD2/remote/inputs"
  }
}

input_json = {
    "entity": {
      "type": "AntibodyDocking",
      "services": {
        "ab_eval_test": {
          "type": "Evaluate",
          "inputs": { 
            "resources": [
              {
                "locationType": "filesystem-path-unix",
                "resourceFormat": "chemical/pdb",
                "resourceRole": "Antibody",
                "payload": "/programs/gems/tests/inputs/UPLOADED_2H1_PDB_MONOMER_.pdb"
              },
              {
                "locationType": "filesystem-path-unix",
                "resourceFormat": "chemical/pdb",
                "resourceRole": "Ligand",
                "payload": "/programs/gems/tests/inputs/DManpa1-8DNeup5Acb2-4DFrufa2-OH_structure.pdb"
              }
            ] 
          }
        }
      }
    }
}

class TestWebsiteExecutionAndAD(unittest.TestCase):
    def setUp(self):
        import gemsModules.project.settings as project_settings
        if "/tmp" not in project_settings.allowed_website_filesystem_paths:
            project_settings.allowed_website_filesystem_paths.append("/tmp")
        os.makedirs("/tmp/testAAD2/remote/ad", exist_ok=True)
        os.makedirs("/tmp/testAAD2/remote/inputs", exist_ok=True)

    def test_suppression_and_delegation(self):
        ic = InstanceConfig(**ic_data)
        self.assertTrue(ic.is_website_environment(), "IC must report website environment")
        set_session_instance_config(ic)
        self.assertTrue(is_stderr_suppressed(), "is_stderr_suppressed() must be True")

        # Capture stderr to guarantee nothing is written
        old_stderr = sys.stderr
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr

        try:
            response_str = receive(json.dumps(input_json))
        finally:
            sys.stderr = old_stderr

        stderr_output = captured_stderr.getvalue()
        self.assertEqual(stderr_output, "", f"Standard error MUST be empty! Got:\n{stderr_output}")

        response_dict = json.loads(response_str)
        self.assertIn("entity", response_dict)
        self.assertIn("project", response_dict)
        print("Test passed successfully! Response generated without stderr output.")
        print(f"Project pUUID: {response_dict['project'].get('pUUID')}")

    def test_exception_suppresses_traceback_on_website(self):
        from unittest.mock import patch
        from gemsModules.complex.antibody.json_string_manager import Antibody_Json_String_Manager

        ic = InstanceConfig(**ic_data)
        set_session_instance_config(ic)
        self.assertTrue(is_stderr_suppressed())

        mgr = Antibody_Json_String_Manager()

        # Force an unexpected exception during transaction processing
        with patch.object(mgr, "transaction_manager_type", side_effect=RuntimeError("Simulated unexpected failure")):
            old_stderr = sys.stderr
            captured_stderr = io.StringIO()
            sys.stderr = captured_stderr
            try:
                result = mgr.process(json.dumps(input_json))
            finally:
                sys.stderr = old_stderr

            # Verify that absolutely nothing was written to stderr
            self.assertEqual(captured_stderr.getvalue(), "")
            self.assertIsNotNone(result)
            err_dict = json.loads(result)
            self.assertIn("notices", err_dict)


if __name__ == "__main__":
    unittest.main()

