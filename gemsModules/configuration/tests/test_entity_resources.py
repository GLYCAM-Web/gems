#!/usr/bin/env python3
import json
import unittest

from gemsModules.configuration.main_api import Host, InstanceConfig, SupportedEntities
from gemsModules.systemoperations.resources_api import Resource, Resources


class TestEntityResourcesConfiguration(unittest.TestCase):

    def test_host_entity_resources(self):
        res_ad = Resource.from_file("/programs/gems/ad_builds", role="AD_Build_Dir", format="Directory")
        resources_list = Resources()
        resources_list.append(res_ad)

        host = Host(
            name="Thoreau",
            address="172.16.4.2",
            is_localhost="True",
            entities_available=[SupportedEntities.ad],
            entity_resources={SupportedEntities.ad: resources_list},
        )

        self.assertIsNotNone(host.entity_resources)
        res_found = host.get_entity_resource(SupportedEntities.ad, "AD_Build_Dir")
        self.assertIsNotNone(res_found)
        self.assertEqual(res_found.payload, "/programs/gems/ad_builds")

    def test_instance_config_filesystem_path_fallback(self):
        ic_dict = {
            "date": "2026-10-04T12:00:00",
            "hosts": [
                {
                    "name": "Localhost",
                    "address": "127.0.0.1",
                    "is_localhost": "True",
                    "entities_available": ["AD"],
                    "entity_resources": {
                        "AD": [
                            {
                                "locationType": "filesystem-path-unix",
                                "resourceRole": "AD_Root",
                                "payload": "/path/to/ad_root",
                            }
                        ]
                    },
                }
            ],
        }

        ic = InstanceConfig(**ic_dict)
        self.assertIsNotNone(ic.hosts)
        path = ic.get_filesystem_path_by_service_ID("AD")
        self.assertEqual(path, "/path/to/ad_root")


if __name__ == "__main__":
    unittest.main()
