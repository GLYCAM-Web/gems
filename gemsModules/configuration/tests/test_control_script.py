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

        generated = generate_from_matrix(str(matrix_path), output_dir=str(self.tmp_path), allow_missing_paths=True)
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
            allow_missing_paths=True,
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

        # Without --allow-missing-paths, missing /scratch/... paths abort
        res_abort = subprocess.run(
            [sys.executable, str(cli), "generate", "--matrix", str(matrix_path), "--output-dir", str(self.tmp_path)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(res_abort.returncode, 0)
        self.assertIn("do not exist on this host", res_abort.stderr)

        res1 = subprocess.run(
            [sys.executable, str(cli), "generate", "--matrix", str(matrix_path), "--output-dir", str(self.tmp_path), "--allow-missing-paths"],
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
                "--allow-missing-paths",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Cloned", res2.stdout)
        ic = InstanceConfig.parse_file(cloned_path)
        self.assertEqual(ic.get_localhost().name, "thoreau-actual")
        self.assertEqual(ic.get_localhost().port, "42053")

    def test_ports_to_matrix_and_generate(self):
        gems_root = Path(__file__).resolve().parents[3]
        cli = gems_root / "bin" / "instance_config.py"
        base_dir = self.tmp_path / "deployments"
        abs_ic = self.tmp_path / "custom_abs_ic.json"

        ports_content = f"""#!/usr/bin/env bash
ServerName="Thoreau"
ServerAddress="172.16.4.2"
base_entities_available="AD GM GP MD"
GEMS_BASE_PATH="{base_dir}"
declare -a serviceIDs
serviceIDs=(
    "alice"
    "bob"
    "actual"
    "paid"
#   "dev"
)
declare -A deploymentID
deploymentID=(
    ["alice"]="visceral-vanbruggen"
    ["bob"]="visceral-vanbruggen"
    ["actual"]="visceral-vanbruggen"
    ["paid"]="sweet-cake"
)
declare -A port_number
port_number=(
    ["alice"]="42050"
    ["bob"]="42050"
    ["actual"]="42054"
    ["paid"]="42060"
)
declare -A gemshome
gemshome=(
    ["alice"]="${{GEMS_BASE_PATH}}/${{deploymentID["alice"]}}/gems"
    ["bob"]="${{GEMS_BASE_PATH}}/${{deploymentID["bob"]}}/gems"
    ["actual"]="${{GEMS_BASE_PATH}}/${{deploymentID["actual"]}}/gems"
    ["paid"]="${{GEMS_BASE_PATH}}/${{deploymentID["paid"]}}/gems"
)
declare -A services
services=(
    ["alice"]="MD"
    ["bob"]="AD"
    ["actual"]=""
    ["paid"]="MD"
)
declare -A instanceconfig
instanceconfig=(
    ["alice"]=""
    ["bob"]=""
    ["actual"]="{abs_ic}"
    ["paid"]="PaidTier/MDaaS.config"
)
"""
        ports_path = self.tmp_path / "PORTS_dat.bash"
        ports_path.write_text(ports_content)
        matrix_path = self.tmp_path / "from_ports_matrix.json"

        subprocess.run(
            [
                sys.executable,
                str(cli),
                "ports-to-matrix",
                str(ports_path),
                "--to",
                str(matrix_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        matrix = json.loads(matrix_path.read_text())
        self.assertEqual(matrix["base"]["name"], "Thoreau")
        self.assertEqual(matrix["base"]["address"], "172.16.4.2")
        # alice and bob share gemshome, port, and instanceconfig -> grouped into 1 variant
        self.assertEqual(len(matrix["variants"]), 3)

        v_test = matrix["variants"][0]
        self.assertEqual(v_test["entities"], ["MD", "AD"])
        self.assertEqual(v_test["port"], "42050")
        self.assertEqual(
            v_test["output"],
            str(base_dir / "visceral-vanbruggen" / "gems" / "instance_config.json"),
        )

        v_actual = matrix["variants"][1]
        self.assertEqual(v_actual["output"], str(abs_ic))

        v_paid = matrix["variants"][2]
        self.assertEqual(
            v_paid["output"],
            str(base_dir / "sweet-cake" / "gems" / "IC" / "PaidTier" / "MDaaS.config"),
        )

        # Feed the generated matrix straight into generate --matrix
        subprocess.run(
            [sys.executable, str(cli), "generate", "--matrix", str(matrix_path), "--allow-missing-paths"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertTrue(abs_ic.exists())
        paid_ic_path = base_dir / "sweet-cake" / "gems" / "IC" / "PaidTier" / "MDaaS.config"
        self.assertTrue(paid_ic_path.exists())
        paid_ic = InstanceConfig.parse_file(paid_ic_path)
        self.assertEqual(paid_ic.get_localhost().port, "42060")
        self.assertEqual([e.value for e in paid_ic.get_localhost().entities_available], ["MD"])

        # Verify relative GEMS_INSTANCE_CONFIG resolves against $GEMSHOME/IC/
        from gemsModules.configuration.user_config import get_effective_instance_config_path
        old_gh = os.environ.get("GEMSHOME")
        old_ic = os.environ.get("GEMS_INSTANCE_CONFIG")
        try:
            os.environ["GEMSHOME"] = str(base_dir / "sweet-cake" / "gems")
            os.environ["GEMS_INSTANCE_CONFIG"] = "PaidTier/MDaaS.config"
            self.assertEqual(get_effective_instance_config_path(), str(paid_ic_path.resolve()))
        finally:
            if old_gh is None:
                os.environ.pop("GEMSHOME", None)
            else:
                os.environ["GEMSHOME"] = old_gh
            if old_ic is None:
                os.environ.pop("GEMS_INSTANCE_CONFIG", None)
            else:
                os.environ["GEMS_INSTANCE_CONFIG"] = old_ic

    def test_ports_to_matrix_single_server_ids(self):
        gems_root = Path(__file__).resolve().parents[3]
        cli = gems_root / "bin" / "instance_config.py"
        base_dir = self.tmp_path / "deployments"

        ports_content = f"""#!/usr/bin/env bash
GEMS_BASE_PATH="{base_dir}"
declare -a serviceIDs
serviceIDs=(
    "devenv"
    "swarmtest"
)
declare -A deploymentID
deploymentID=(
    ["devenv"]="developer-environment"
    ["swarmtest"]="sweet-cake"
)
declare -A port_number
port_number=(
    ["devenv"]="42054"
    ["swarmtest"]="42053"
)
declare -A gemshome
gemshome=(
    ["devenv"]="${{GEMS_BASE_PATH}}/${{deploymentID["devenv"]}}/gems"
    ["swarmtest"]="${{GEMS_BASE_PATH}}/${{deploymentID["swarmtest"]}}/gems"
)
declare -A instanceconfig
instanceconfig=(
    ["devenv"]=""
    ["swarmtest"]=""
)
"""
        ports_path = self.tmp_path / "PORTS_simple.bash"
        ports_path.write_text(ports_content)
        matrix_path = self.tmp_path / "simple_matrix.json"

        subprocess.run(
            [sys.executable, str(cli), "ports-to-matrix", str(ports_path), "--to", str(matrix_path), "--cluster-name", "Thoreau"],
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(
            [sys.executable, str(cli), "generate", "--matrix", str(matrix_path), "--allow-missing-paths"],
            capture_output=True,
            text=True,
            check=True,
        )
        st_ic = InstanceConfig.parse_file(base_dir / "sweet-cake" / "gems" / "instance_config.json")
        self.assertEqual(st_ic.get_localhost().port, "42053")
        self.assertEqual([e.value for e in st_ic.get_localhost().entities_available], ["AD", "GM", "GP", "MD"])

    def test_cluster_base_website_dict_and_service_id_filter(self):
        gems_root = Path(__file__).resolve().parents[3]
        cli = gems_root / "bin" / "instance_config.py"
        base_dir = self.tmp_path / "deployments"

        cluster_base = {
            "name": "Thoreau",
            "name_template": "Thoreau-{id}",
            "address": "172.16.4.2",
            "scheduler": "slurm",
            "execution_environments": ["Batch", "Standalone"],
            "entities_available": ["AD", "GM", "GP", "MD"],
            "batch_computing_resources": [
                {
                    "partition": "wCPU",
                    "supported_entities": ["AD", "GM", "GP"],
                    "max_nodes_per_job": "1",
                    "max_cores_per_node": "28",
                    "max_threads_per_node": "28",
                    "max_gpus_per_node": "0",
                    "max_cpus_per_gpu": "0",
                    "max_time_limit": "P2D",
                },
                {
                    "partition": "wGPU",
                    "supported_entities": ["MD"],
                    "max_nodes_per_job": "1",
                    "max_cores_per_node": "4",
                    "max_threads_per_node": "4",
                    "max_gpus_per_node": "4",
                    "max_cpus_per_gpu": "1",
                    "max_time_limit": "P2DT16H30M",
                },
            ],
            "filesystem_path_template": "/scratch1/thoreau-web/userdata/{site}/{entity}",
            "secure_inputs_path_template": "/scratch1/thoreau-web/uploads/{site}/{entity}",
        }
        base_path = self.tmp_path / "thoreau_base.json"
        base_path.write_text(json.dumps(cluster_base))

        ports_content = f"""#!/usr/bin/env bash
ServerName="Thoreau"
ServerAddress="172.16.4.2"
base_entities_available="AD GM GP MD"
GEMS_BASE_PATH="{base_dir}"
declare -a serviceIDs
serviceIDs=(
    "test"
    "test-tmp"
)
declare -A port_number
port_number=(
    ["test"]="42050"
    ["test-tmp"]="42060"
)
declare -A gemshome
gemshome=(
    ["test"]="${{GEMS_BASE_PATH}}/xenial-xa/gems"
    ["test-tmp"]="${{GEMS_BASE_PATH}}/xenial-xa-temp/gems"
)
declare -A services
services=(
    ["test"]="GM GP MD"
    ["test-tmp"]="AD"
)
declare -A website
website=(
    ["test-tmp"]="test"
)
declare -A instanceconfig
instanceconfig=(
    ["test"]=""
    ["test-tmp"]=""
)
"""
        ports_path = self.tmp_path / "PORTS_dat.bash"
        ports_path.write_text(ports_content)
        matrix_path = self.tmp_path / "filtered_matrix.json"

        subprocess.run(
            [
                sys.executable,
                str(cli),
                "ports-to-matrix",
                str(ports_path),
                "--cluster-base",
                str(base_path),
                "--service-id",
                "test-tmp",
                "--to",
                str(matrix_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(cli),
                "generate",
                "--matrix",
                str(matrix_path),
                "--service-id",
                "test-tmp",
                "--allow-missing-paths",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Only test-tmp should be generated; test should not exist
        self.assertFalse((base_dir / "xenial-xa" / "gems" / "instance_config.json").exists())
        tmp_ic = InstanceConfig.parse_file(base_dir / "xenial-xa-temp" / "gems" / "instance_config.json")
        lh = tmp_ic.get_localhost()
        self.assertEqual(lh.name, "Thoreau-test-tmp")
        self.assertEqual(lh.port, "42060")
        self.assertEqual([e.value for e in lh.entities_available], ["AD"])
        self.assertEqual(len(lh.batch_computing_resources), 1)
        self.assertEqual(lh.batch_computing_resources[0].partition, "wCPU")
        self.assertEqual(lh.batch_computing_resources[0].max_time_limit, "P2D")
        # website["test-tmp"]="test" -> {site} resolves to "test", not "test-tmp"
        self.assertEqual(tmp_ic.get_filesystem_path_by_service_ID("AD"), "/scratch1/thoreau-web/userdata/test/AD")
        self.assertEqual(tmp_ic.get_secure_inputs_path_by_service_ID("AD"), "/scratch1/thoreau-web/uploads/test/AD")


if __name__ == "__main__":
    unittest.main()
