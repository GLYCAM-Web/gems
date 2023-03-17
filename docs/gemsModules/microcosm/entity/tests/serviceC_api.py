#!/usr/bin/env python3
from gemsModules.docs.microcosm.entity import serviceC_api as api

print(api.inputs.schema_json(indent=2))
print(api.outputs.schema_json(indent=2))
