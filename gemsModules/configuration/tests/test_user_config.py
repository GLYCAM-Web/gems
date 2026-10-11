#!/usr/bin/env python3
import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from gemsModules.configuration import user_config
from gemsModules.configuration.user_config import (
    find_gemsrc_path,
    parse_gemsrc,
    load_gemsrc,
    get_gemsrc_value,
    get_effective_gemshome,
    get_effective_logs_dir,
    get_effective_instance_config_path,
    get_effective_output_dir,
    get_effective_uploads_dir,
    get_effective_logging_level,
    generate_sample_gemsrc,
    is_directory_writable,
)
from gemsModules.logging.logger import Set_Up_Logging
from gemsModules.systemoperations.environment_ops import get_gems_path, find_instance_config
from gemsModules.project.main_api import Project


class TestUserConfig(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.old_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        # Reset cache
        user_config.load_gemsrc(force_reload=True)

    def test_parse_gemsrc_json(self):
        rc_path = os.path.join(self.temp_dir, ".gemsrc")
        custom_out = os.path.join(self.temp_dir, "custom_out")
        custom_logs = os.path.join(self.temp_dir, "custom_logs")
        with open(rc_path, "w") as f:
            json.dump({
                "output_dir": custom_out,
                "log_dir": custom_logs,
                "logging_level": "debug",
                "instance_config": "/path/to/custom_ic.json"
            }, f)

        cfg = parse_gemsrc(rc_path)
        self.assertEqual(cfg["output_dir"], custom_out)
        self.assertEqual(cfg["log_dir"], custom_logs)
        self.assertEqual(cfg["logging_level"], "debug")
        self.assertEqual(cfg["instance_config"], "/path/to/custom_ic.json")

    def test_parse_gemsrc_ini(self):
        rc_path = os.path.join(self.temp_dir, ".gemsrc")
        custom_out = os.path.join(self.temp_dir, "custom_ini_out")
        with open(rc_path, "w") as f:
            f.write(f"""
[gems]
output_dir = {custom_out}
logging_level = info
instance_config = /opt/instance_config.json
""")

        cfg = parse_gemsrc(rc_path)
        self.assertEqual(cfg["output_dir"], custom_out)
        self.assertEqual(cfg["logging_level"], "info")
        self.assertEqual(cfg["instance_config"], "/opt/instance_config.json")

    def test_find_gemsrc_via_env(self):
        rc_path = os.path.join(self.temp_dir, "my_custom_gemsrc")
        with open(rc_path, "w") as f:
            f.write('{"output_dir": "/tmp/custom"}')

        os.environ["GEMS_RC"] = rc_path
        found = find_gemsrc_path()
        self.assertEqual(str(found), str(Path(rc_path).resolve()))

        load_gemsrc(force_reload=True)
        self.assertEqual(get_gemsrc_value("output_dir"), "/tmp/custom")

    def test_effective_gemshome_autodetection(self):
        if "GEMSHOME" in os.environ:
            del os.environ["GEMSHOME"]
        user_config.load_gemsrc(force_reload=True)

        home = get_effective_gemshome()
        self.assertTrue(os.path.isdir(home))
        self.assertTrue(os.path.isdir(os.path.join(home, "gemsModules")))
        self.assertEqual(get_gems_path(), home)

    def test_effective_logs_dir_respects_gemsrc(self):
        custom_logs = os.path.join(self.temp_dir, "logs")
        os.makedirs(custom_logs, exist_ok=True)
        rc_path = os.path.join(self.temp_dir, ".gemsrc")
        with open(rc_path, "w") as f:
            json.dump({"log_dir": custom_logs}, f)

        os.environ["GEMS_RC"] = rc_path
        load_gemsrc(force_reload=True)

        effective_log = get_effective_logs_dir()
        self.assertEqual(effective_log, custom_logs)

    def test_effective_instance_config_search_order(self):
        # 1. Test .gemsrc override
        custom_ic = os.path.join(self.temp_dir, "test_ic.json")
        with open(custom_ic, "w") as f:
            f.write("{}")

        rc_path = os.path.join(self.temp_dir, ".gemsrc")
        with open(rc_path, "w") as f:
            json.dump({"instance_config": custom_ic}, f)

        os.environ["GEMS_RC"] = rc_path
        load_gemsrc(force_reload=True)

        self.assertEqual(get_effective_instance_config_path(), custom_ic)
        self.assertEqual(find_instance_config(), custom_ic)

        # 2. Test environment variable override over .gemsrc
        env_ic = os.path.join(self.temp_dir, "env_ic.json")
        with open(env_ic, "w") as f:
            f.write("{}")
        os.environ["GEMS_INSTANCE_CONFIG"] = env_ic
        self.assertEqual(get_effective_instance_config_path(), env_ic)

    def test_logger_creates_without_crash_when_gemshome_unset(self):
        if "GEMSHOME" in os.environ:
            del os.environ["GEMSHOME"]
        user_config.load_gemsrc(force_reload=True)

        log = Set_Up_Logging("test_standalone_logger")
        self.assertIsNotNone(log)
        # Verify writing log messages does not throw
        log.info("Testing standalone logger info message")
        log.error("Testing standalone logger error message")

    def test_project_output_dir_uses_user_config(self):
        custom_out = os.path.join(self.temp_dir, "my_projects")
        custom_uploads = os.path.join(self.temp_dir, "my_uploads")
        os.makedirs(custom_out, exist_ok=True)
        os.makedirs(custom_uploads, exist_ok=True)

        rc_path = os.path.join(self.temp_dir, ".gemsrc")
        with open(rc_path, "w") as f:
            json.dump({
                "output_dir": custom_out,
                "uploads_dir": custom_uploads
            }, f)

        os.environ["GEMS_RC"] = rc_path
        # Clear live swarm context so it runs in standalone context
        if "GW_LIVE_SWARM" in os.environ:
            del os.environ["GW_LIVE_SWARM"]
        load_gemsrc(force_reload=True)

        proj = Project()
        proj.add_filesystem_info()
        self.assertEqual(proj.filesystem_path, custom_out)
        self.assertEqual(proj.uploads_path, custom_uploads)

    def test_generate_sample_gemsrc(self):
        out_path = os.path.join(self.temp_dir, "sample_gemsrc")
        content = generate_sample_gemsrc(out_path)
        self.assertTrue(os.path.exists(out_path))
        self.assertIn("[gems]", content)
        self.assertIn("log_dir", content)
        self.assertIn("output_dir", content)


if __name__ == "__main__":
    unittest.main()
