import unittest
import json
from gemsModules.common.main_api_provenance import (
    HostContext,
    Provenance,
    translate_path_prefix,
    translate_request_paths,
    translate_response_paths,
)
from gemsModules.common.main_api import Common_API
from gemsModules.project.main_api import Project


class TestProvenanceAndPathTranslation(unittest.TestCase):

    def test_translate_path_prefix(self):
        # Forward translation
        from_prefix = "/website/uploads"
        to_prefix = "/scratch2/thoreau-web/DevEnv/uploads"
        p = "/website/uploads/tools/ad/git-ignore-me_userdata/4ddd79aa/structure.pdb"
        expected = "/scratch2/thoreau-web/DevEnv/uploads/tools/ad/git-ignore-me_userdata/4ddd79aa/structure.pdb"
        self.assertEqual(translate_path_prefix(p, from_prefix, to_prefix), expected)

        # Reverse translation
        from_fs = "/scratch2/thoreau-web/DevEnv/userdata"
        to_fs = "/website/userdata"
        out_p = "/scratch2/thoreau-web/DevEnv/userdata/complex/ad/uuid-1234/Complex.pdb"
        expected_out = "/website/userdata/complex/ad/uuid-1234/Complex.pdb"
        self.assertEqual(translate_path_prefix(out_p, from_fs, to_fs), expected_out)

        # Trailing slash tolerance
        self.assertEqual(
            translate_path_prefix(p, "/website/uploads/", "/scratch2/thoreau-web/DevEnv/uploads/"),
            expected
        )

        # No match leaves path untouched
        other_path = "/programs/website/deployment/tests/test.pdb"
        self.assertEqual(translate_path_prefix(other_path, from_prefix, to_prefix), other_path)

        # Boundary safety (does not partially match directory name)
        partial_dir = "/website/uploads_archive/file.pdb"
        self.assertEqual(translate_path_prefix(partial_dir, from_prefix, to_prefix), partial_dir)

        # Identity
        self.assertEqual(translate_path_prefix(p, from_prefix, from_prefix), p)
        self.assertEqual(translate_path_prefix(None, from_prefix, to_prefix), None)

    def test_translate_request_paths(self):
        request_dict = {
            "entity": {
                "type": "AntibodyDocking",
                "services": {
                    "Evaluate": {
                        "inputs": {
                            "antibody_path": "/website/uploads/tools/ad/uuid/ab.pdb",
                            "ligand_path": "/website/uploads/tools/ad/uuid/lig.pdb",
                            "resources": [
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "resourceRole": "Antibody",
                                    "payload": "/website/uploads/tools/ad/uuid/ab.pdb"
                                },
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "resourceRole": "Ligand",
                                    "payload": "/website/uploads/tools/ad/uuid/lig.pdb"
                                },
                                {
                                    "locationType": "Payload",
                                    "resourceFormat": "string",
                                    "resourceRole": "Metadata",
                                    "payload": "raw string content"
                                }
                            ]
                        }
                    }
                }
            },
            "project": {
                "uploads_path": "/website/uploads",
                "filesystem_path": "/website/userdata",
                "project_dir": "/website/userdata/complex/ad/uuid",
            }
        }

        translated = translate_request_paths(
            request_dict,
            from_secure="/website/uploads",
            to_secure="/scratch2/thoreau-web/DevEnv/uploads",
            from_fs="/website/userdata",
            to_fs="/scratch2/thoreau-web/DevEnv/userdata"
        )

        eval_inputs = translated["entity"]["services"]["Evaluate"]["inputs"]
        self.assertEqual(
            eval_inputs["antibody_path"],
            "/scratch2/thoreau-web/DevEnv/uploads/tools/ad/uuid/ab.pdb"
        )
        self.assertEqual(
            eval_inputs["resources"][0]["payload"],
            "/scratch2/thoreau-web/DevEnv/uploads/tools/ad/uuid/ab.pdb"
        )
        self.assertEqual(
            eval_inputs["resources"][1]["payload"],
            "/scratch2/thoreau-web/DevEnv/uploads/tools/ad/uuid/lig.pdb"
        )
        # Non-file payload untouched
        self.assertEqual(eval_inputs["resources"][2]["payload"], "raw string content")

        # Project paths translated
        self.assertEqual(translated["project"]["uploads_path"], "/scratch2/thoreau-web/DevEnv/uploads")
        self.assertEqual(translated["project"]["filesystem_path"], "/scratch2/thoreau-web/DevEnv/userdata")
        self.assertEqual(translated["project"]["project_dir"], "/scratch2/thoreau-web/DevEnv/userdata/complex/ad/uuid")

    def test_translate_response_paths(self):
        response_dict = {
            "entity": {
                "type": "AntibodyDocking",
                "responses": {
                    "Evaluate": {
                        "outputs": {
                            "status": "Success",
                            "resources": [
                                {
                                    "locationType": "filesystem-path-unix",
                                    "resourceFormat": "chemical/pdb",
                                    "payload": "/scratch2/thoreau-web/DevEnv/userdata/complex/ad/uuid/Complex.pdb"
                                }
                            ]
                        }
                    }
                }
            },
            "project": {
                "filesystem_path": "/scratch2/thoreau-web/DevEnv/userdata",
                "project_dir": "/scratch2/thoreau-web/DevEnv/userdata/complex/ad/uuid",
            }
        }

        translated = translate_response_paths(
            response_dict,
            from_fs="/scratch2/thoreau-web/DevEnv/userdata",
            to_fs="/website/userdata",
            from_secure="/scratch2/thoreau-web/DevEnv/uploads",
            to_secure="/website/uploads",
        )

        res_payload = translated["entity"]["responses"]["Evaluate"]["outputs"]["resources"][0]["payload"]
        self.assertEqual(res_payload, "/website/userdata/complex/ad/uuid/Complex.pdb")
        self.assertEqual(translated["project"]["project_dir"], "/website/userdata/complex/ad/uuid")
        self.assertEqual(translated["project"]["filesystem_path"], "/website/userdata")

    def test_common_api_provenance_sync(self):
        # Sync from legacy fields to Provenance
        api = Common_API(
            entity={"type": "CommonServicer"},
            initial_receiver="DevEnv-Web",
            execution_host="Thoreau",
            initiation_timestamp="2026-10-13_01:00:00"
        )
        self.assertIsNotNone(api.provenance)
        self.assertEqual(api.provenance.initial_receiver.name, "DevEnv-Web")
        self.assertEqual(api.provenance.execution_host.name, "Thoreau")
        self.assertEqual(api.provenance.initial_receiver.timestamp, "2026-10-13_01:00:00")

        # Sync from Provenance to legacy fields
        prov = Provenance(
            initial_receiver=HostContext(
                name="HostA",
                timestamp="2026-10-13_02:00:00",
                secure_inputs_path="/uploads/a",
                filesystem_path="/userdata/a"
            ),
            execution_host=HostContext(
                name="HostB",
                timestamp="2026-10-13_02:00:05",
                secure_inputs_path="/uploads/b",
                filesystem_path="/userdata/b"
            )
        )
        api2 = Common_API(
            entity={"type": "CommonServicer"},
            provenance=prov
        )
        self.assertEqual(api2.initial_receiver, "HostA")
        self.assertEqual(api2.execution_host, "HostB")
        self.assertEqual(api2.initiation_timestamp, "2026-10-13_02:00:00")

    def test_delegator_receive_provenance(self):
        from gemsModules.delegator.receive import receive
        req = {
            "entity": {
                "type": "Delegator",
                "services": {
                    "Marco": {
                        "type": "Marco"
                    }
                }
            }
        }
        res_str = receive(json.dumps(req))
        res = json.loads(res_str)
        self.assertIn("provenance", res)
        self.assertIn("initial_receiver", res["provenance"])
        self.assertIn("execution_host", res["provenance"])
        self.assertTrue(len(res["provenance"]["initial_receiver"]["name"]) > 0)
        self.assertTrue(len(res["provenance"]["execution_host"]["name"]) > 0)
        self.assertIn("initial_receiver", res)
        self.assertIn("execution_host", res)
        self.assertEqual(res["entity"]["responses"]["Marco"]["outputs"]["message"], "Polo")


if __name__ == "__main__":
    unittest.main()

