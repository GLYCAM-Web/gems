import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from gemsModules.configuration.control_script import clone_ic, generate_from_matrix
from gemsModules.configuration.main_api import InstanceConfig


class TestControlScriptMatrixAndClone(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp_dir.name)

    def tearDown(self):
        # Ensure read-only files can be cleaned up by TemporaryDirectory
        for root, _, files in os.walk(self.tmp_path):
            for name in files:
                p = os.path.join(root, name)
                try:
                    os.chmod(p, 0o644)
                except Exception:
                    pass
        self.tmp_dir.cleanup()

    def test_generate_from_matrix_four_plus_split(self):
        matrix = {
            "base": {
                "name": "thoreau",
                "address": "172.16.4.2",
                "scheduler": "slurm",
                "execution_environments": ["Batch", "Standalone"],
                "entities_available": ["AD", "GM", "MD"],
                "batch_computing_resources": [
                    {
                        "partition": "amber",
                        "supported_entities": ["AD", "MD"],
                        "max_nodes_per_job": "1",
                        "max_cores_per_node": "4",
                    },
                    {
                        "partition": "gm",
                        "supported_entities": ["GM"],
                        "max_nodes_per_job": "1",
                        "max_cores_per_node": "8",
                    },
                ],
                "resource_specific_information": {
                    "use_gres_for_gpus": "True",
                    "cpu_hardware_equivalent": "core",
                    "aad2_configuration": {
                        "aad2_docker_home": "/programs/website_aad2/{env}/AAD2_Docker"
                    },
                },
                "filesystem_path_template": "/scratch/gems/{id}/{entity}",
                "secure_inputs_path_template": "/scratch/gems/{id}/{entity}/inputs",
            },
            "variants": [
                {"id": "swarmtest", "env": "swarmtest", "port": "42050"},
                {"id": "actual", "env": "actual", "port": "42053"},
                {
                    "id": "ad-actual",
                    "env": "actual",
                    "port": "42063",
                    "entities": ["AD"],
                    "output": "instance_config.ad-actual.json",
                },
            ],
        }
        matrix_path = self.tmp_path / "matrix.json"
        matrix_path.write_text(json.dumps(matrix))

        generated = generate_from_matrix(str(matrix_path), output_dir=str(self.tmp_path))
        self.assertEqual(len(generated), 3)

        # Verify swarmtest variant
        st_ic = InstanceConfig.parse_file(self.tmp_path / "instance_config.swarmtest.json")
        st_host = st_ic.get_localhost()
        self.assertEqual(st_host.name, "thoreau-swarmtest")
        self.assertEqual(st_host.port, "42050")
        self.assertEqual(st_host.get_aad2_configuration().aad2_docker_home, "/programs/website_aad2/swarmtest/AAD2_Docker")
        self.assertEqual(st_ic.get_filesystem_path_by_service_ID("MD"), "/scratch/gems/swarmtest/MD")
        self.assertEqual(st_ic.get_secure_inputs_path_by_service_ID("AD"), "/scratch/gems/swarmtest/AD/inputs")

        # Verify AD-only split variant scopes partitions and paths
        ad_ic = InstanceConfig.parse_file(self.tmp_path / "instance_config.ad-actual.json")
        ad_host = ad_ic.get_localhost()
        self.assertEqual(ad_host.name, "thoreau-ad-actual")
        self.assertEqual(ad_host.port, "42063")
        self.assertEqual([e.value for e in ad_host.entities_available], ["AD"])
        self.assertEqual(len(ad_host.batch_computing_resources), 1)
        self.assertEqual(ad_host.batch_computing_resources[0].partition, "amber")
        self.assertEqual([e.value for e in ad_host.batch_computing_resources[0].supported_entities], ["AD"])
        self.assertEqual(ad_ic.get_filesystem_path_by_service_ID("AD"), "/scratch/gems/ad-actual/AD")
        self.assertIsNone(ad_ic.get_filesystem_path_by_service_ID("MD"))

        # Verify files are marked read-only (0o444)
        mode = stat.S_IMODE(os.stat(self.tmp_path / "instance_config.ad-actual.json").st_mode)
        self.assertEqual(mode, 0o444)

    def test_clone_ic_with_overrides(self):
        src_ic = {
            "date": "2026-10-11T00:00:00",
            "hosts": [
                {
                    "name": "thoreau-actual",
                    "address": "172.16.4.2",
                    "port": "42053",
                    "is_localhost": "True",
                    "scheduler": "slurm",
                    "execution_environments": ["Batch", "Standalone"],
                    "entities_available": ["AD", "MD"],
                    "batch_computing_resources": [
                        {
                            "partition": "amber",
                            "supported_entities": ["AD", "MD"],
                            "max_nodes_per_job": "1",
                            "max_cores_per_node": "4",
                        }
                    ],
                    "resource_specific_information": {
                        "use_gres_for_gpus": "True",
                        "cpu_hardware_equivalent": "core",
                        "aad2_configuration": {
                            "aad2_docker_home": "/programs/website_aad2/actual/AAD2_Docker"
                        },
                    },
                },
                {
                    "name": "website-host",
                    "address": "10.0.0.5",
                    "is_localhost": "False",
                    "entities_available": ["CB"],
                },
            ],
            "filesystem_paths": {"AD": "/scratch/actual/AD", "MD": "/scratch/actual/MD"},
            "secure_inputs_paths": {"AD": "/scratch/actual/AD/inputs", "MD": "/scratch/actual/MD/inputs"},
        }
        src_path = self.tmp_path / "src.json"
        src_path.write_text(json.dumps(src_ic))
        dest_path = self.tmp_path / "cloned.json"

        clone_ic(
            source_path=str(src_path),
            dest_path=str(dest_path),
            name="thoreau-ad-test",
            port="42061",
            entities=["AD"],
            fs_template="/scratch/ad-test/{entity}",
            inputs_template="/scratch/ad-test/{entity}/inputs",
            aad2_home="/programs/website_aad2/test/AAD2_Docker",
            sets=["resource_specific_information.cpu_hardware_equivalent=thread"],
            drop_remote_hosts=True,
        )

        cloned = InstanceConfig.parse_file(dest_path)
        self.assertEqual(len(cloned.hosts), 1)
        lh = cloned.get_localhost()
        self.assertEqual(lh.name, "thoreau-ad-test")
        self.assertEqual(lh.port, "42061")
        self.assertEqual([e.value for e in lh.entities_available], ["AD"])
        self.assertEqual([e.value for e in lh.batch_computing_resources[0].supported_entities], ["AD"])
        self.assertEqual(lh.get_aad2_configuration().aad2_docker_home, "/programs/website_aad2/test/AAD2_Docker")
        self.assertEqual(lh.resource_specific_information.cpu_hardware_equivalent, "thread")
        self.assertEqual(cloned.get_filesystem_path_by_service_ID("AD"), "/scratch/ad-test/AD")
        self.assertIsNone(cloned.get_filesystem_path_by_service_ID("MD"))

    def test_cli_matrix_and_clone(self):
        gems_root = Path(__file__).resolve().parents[3]
        cli = gems_root / "bin" / "instance_config.py"
        matrix = {
            "base": {
                "name": "thoreau",
                "address": "172.16.4.2",
                "entities_available": ["AD", "MD"],
                "filesystem_path_template": "/scratch/{id}/{entity}",
            },
            "variants": [{"id": "swarmtest", "port": "42050"}],
        }
        matrix_path = self.tmp_path / "cli_matrix.json"
        matrix_path.write_text(json.dumps(matrix))

        res1 = subprocess.run(
            [sys.executable, str(cli), "generate", "--matrix", str(matrix_path), "--output-dir", str(self.tmp_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Generated", res1.stdout)

        cloned_path = self.tmp_path / "cli_cloned.json"
        res2 = subprocess.run(
            [
                sys.executable,
                str(cli),
                "clone",
                str(self.tmp_path / "instance_config.swarmtest.json"),
                "--to",
                str(cloned_path),
                "--name",
                "thoreau-actual",
                "--port",
                "42053",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Cloned", res2.stdout)
        ic = InstanceConfig.parse_file(cloned_path)
        self.assertEqual(ic.get_localhost().name, "thoreau-actual")
        self.assertEqual(ic.get_localhost().port, "42053")


if __name__ == "__main__":
    unittest.main()
