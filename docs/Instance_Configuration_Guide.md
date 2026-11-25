# Instance Configuration (IC) Guide

This guide explains how to generate and connect GEMS Instance Configuration (`instance_config.json`) files for:

1. **A compute host / cluster** (e.g., Thoreau) accepting services such as `AD` and `MD`.
2. **A website-facing GEMS** that delegates `AD` and `MD` jobs to that cluster over gRPC.

All commands below are run from `$GEMSHOME` using `./bin/instance_config.py`.

---

## 1. Cluster-Side IC (e.g., Thoreau)

### Method A: From `PORTS_dat.bash` (`ports-to-matrix` → `generate --matrix`)

If you use `webGRPC` with a `PORTS_dat.bash` file, you can generate a matrix skeleton directly from it and stamp out all ICs at once.

#### Step 1: Create a cluster base file (once per cluster)
Static cluster hardware and website-keyed path templates live in a reusable JSON file (e.g., `thoreau_base.json`). The file can be either a flat object or wrapped in `{"base": { ... }}`:

```json
{
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
      "max_time_limit": "P2D"
    },
    {
      "partition": "wGPU",
      "supported_entities": ["MD"],
      "max_nodes_per_job": "1",
      "max_cores_per_node": "4",
      "max_threads_per_node": "4",
      "max_gpus_per_node": "4",
      "max_cpus_per_gpu": "1",
      "max_time_limit": "P2DT16H30M"
    }
  ],
  "resource_specific_information": {
    "use_gres_for_gpus": "True",
    "cpu_hardware_equivalent": "core",
    "aad2_configuration": {
      "aad2_docker_home": "/programs/website_aad2/{site}/AAD2_Docker"
    }
  },
  "filesystem_path_template": "/scratch1/thoreau-web/userdata/{site}/{entity}",
  "secure_inputs_path_template": "/scratch1/thoreau-web/uploads/{site}/{entity}"
}
```

- **`max_time_limit`**: Uses ISO 8601 duration strings (e.g., `PT2H`, `P2D`, `P2DT16H30M`), which GEMS converts to Slurm `--time` format (`HH:MM:SS` or `D-HH:MM:SS`) when submitting jobs.
- **`{site}` placeholder**: Resolves to `website[serviceID]` from `PORTS_dat.bash` if set (e.g., `website["test-tmp"]="test"`), or `serviceID` itself if omitted. This ensures uploads and outputs follow the website (`test`, `dev`, `actual`, `swarmtest`) rather than the deployment codename.

#### Step 2: Generate the matrix (all or a single `--service-id`)
```bash
# All active serviceIDs in PORTS_dat.bash:
./bin/instance_config.py ports-to-matrix /path/to/PORTS_dat.bash \
  --cluster-base thoreau_base.json \
  --to thoreau_matrix.json

# Or just one deployment (e.g. when promoting to dev):
./bin/instance_config.py ports-to-matrix /path/to/PORTS_dat.bash \
  --cluster-base thoreau_base.json \
  --service-id dev \
  --to dev_matrix.json
```

This reads `ServerName`, `ServerAddress`, `base_entities_available`, `serviceIDs`, `port_number`, `gemshome`, `services`, `website`, and `instanceconfig` from `PORTS_dat.bash`, merges them with `thoreau_base.json`, and writes the matrix file.

> **Tip (`name_template`)**: If multiple variants on the same cluster (for example, `test` for `MD` on port `42050` and `test-tmp` for `AD` on port `42060`) will be imported into the **same** website IC, give them distinct host names (such as `"name_template": "Thoreau-{id}"`) so one import does not overwrite the other.

#### Step 3: Generate and validate the IC files
```bash
# Generate all variants in the matrix:
./bin/instance_config.py generate --matrix thoreau_matrix.json

# Or generate only a specific variant from an existing matrix:
./bin/instance_config.py generate --matrix thoreau_matrix.json --service-id dev
```

Each variant is validated against `InstanceConfig` and written read-only (`0o444`) to its `output` path:
- If `instanceconfig[id]` in `PORTS_dat.bash` was empty: `$GEMSHOME/instance_config.json`
- If `instanceconfig[id]` was relative (e.g., `PaidTier/MDaaS.config`): `$GEMSHOME/IC/<instanceconfig>`
- If `instanceconfig[id]` was absolute: that exact path

#### Step 4: Verify the generated IC
```bash
./bin/instance_config.py validate --ic-file /path/to/instance_config.json
./bin/instance_config.py evaluate --ic-file /path/to/instance_config.json
```

---

### Method B: Cloning an Existing IC (`clone`)

When you already have one working IC and want a quick variant (e.g., splitting `AD` onto a separate port/GEMS):

```bash
./bin/instance_config.py clone /path/to/instance_config.json \
  --to /path/to/IC/ad_only.json \
  --name Thoreau-AD \
  --port 42060 \
  --entities AD \
  --fs-template "/scratch/gems/ad-only/{entity}" \
  --inputs-template "/scratch/gems/ad-only/{entity}/inputs"
```

Use `--set KEY=VALUE` (repeatable) for any nested localhost field, e.g. `--set resource_specific_information.use_gres_for_gpus=False`.

---

### Method C: Interactive TUI (`generate --use-tui`)

For a single standalone or first-time IC without a matrix:
```bash
./bin/instance_config.py generate --use-tui
```

---

## 2. Website-Side IC (Contacting Thoreau for `AD` and `MD`)

The website's GEMS needs its own local `instance_config.json` defining itself as `is_localhost: "True"` (with `execution_environments` including `"Website"`, `website_environments` set to e.g. `["Test"]` / `["Dev"]` / `["Actual"]` / `["SwarmTest"]`, and local `filesystem_paths` / `secure_inputs_paths` for `AD`, `MD`, etc.).

Once the website's base `instance_config.json` exists and Thoreau's gRPC server(s) are running, import Thoreau's host entry into the website's IC using either **gRPC pull** or **file export/import**.

### Option A: Pull Directly Over gRPC (`import --from-remote` or `import --from-ports`)

Run this on the **website GEMS** (use `--ic-file` / `--using-ic` to target a non-default IC such as `IC/IC_delegator.json`; relative names are resolved against CWD or `$GEMSHOME/IC/`):
```bash
./bin/instance_config.py import --from-remote 172.16.4.2:42053 --ic-file IC/IC_delegator.json
# Or using a relative name inside $GEMSHOME/IC/:
./bin/instance_config.py import --from-remote 172.16.4.2:42053 --using-ic IC_delegator.json
```

If `PORTS_dat.bash` (containing `ServerAddress` and `port_number`) is visible to the website, you can import directly from it:
```bash
./bin/instance_config.py import --from-ports /path/to/PORTS_dat.bash --service-id swarmtest --using-ic IC_delegator.json
```

- If `GEMS_INSTANCE_CONFIG` is set and `--ic-file` / `--using-ic` is omitted, `import`, `export`, `validate`, `evaluate`, `report`, `check-connectivity`, `confirm-capabilities`, and `status` all pick up `GEMS_INSTANCE_CONFIG` automatically.
- `import` sends a gRPC `ExportHost` (`target: "localhost"`) request to the remote GEMS, receives its host capabilities, forces `is_localhost` to `"False"`, merges it into the target IC, and validates the result.

### Option B: Offline File Export / Import (`export` → `import --from-file`)

If the website cannot reach Thoreau directly while staging configs:

1. On **Thoreau**:
   ```bash
   ./bin/instance_config.py export localhost --ic-file /path/to/instance_config.json --to-file thoreau_export.json
   ```
2. Copy `thoreau_export.json` to the **website GEMS** and run:
   ```bash
   ./bin/instance_config.py import --from-file thoreau_export.json --ic-file IC/IC_delegator.json
   ```

### Verify From the Website GEMS
```bash
./bin/instance_config.py evaluate --ic-file IC/IC_delegator.json
./bin/instance_config.py check-connectivity Thoreau-swarmtest --ic-file IC/IC_delegator.json
./bin/instance_config.py confirm-capabilities Thoreau-swarmtest --ic-file IC/IC_delegator.json
./bin/instance_config.py status --ic-file IC/IC_delegator.json
```

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pydantic'` when `json_server.py` invokes `bin/delegate`**:
  `bin/delegate` automatically activates `$GEMSHOME/.venv` if present, otherwise falling back to system `python3`. Run `bash bin/setup-venv.sh` (or `bash bin/setup-venv.sh --python python3.11`) in `$GEMSHOME` on the cluster.
- **`ImportError: /lib64/libstdc++.so.6: version 'GLIBCXX_3.4.xx' not found` (required by `_gmml.so`)**:
  `gmml` was compiled with a newer GCC than the OS system `libstdc++`. Add that GCC's `lib64` directory (e.g. `/opt/ohpc/pub/compiler/gcc/12.4.0/lib64`) to `LD_LIBRARY_PATH` in the systemd service unit (or `PORTS_dat.bash` `ld_library_path`).
- **Missing local paths during `generate --matrix` / `clone`**:
  By default, IC generation aborts if configured local `filesystem_paths`, `secure_inputs_paths`, or `aad2_docker_home` do not exist on disk. Create the directories first or pass `--allow-missing-paths` if staging offline.

---

## Related Documentation
- [`User_Configuration_and_Standalone_GEMS.md`](User_Configuration_and_Standalone_GEMS.md) — `.gemsrc`, `GEMS_INSTANCE_CONFIG`, and `$GEMSHOME/IC/` lookup order.
- [`GEMS_to_GEMS_Communication.md`](GEMS_to_GEMS_Communication.md) — Overview of gRPC communication between GEMS instances.
- [`../gemsModules/configuration/Design_Doc.md`](../gemsModules/configuration/Design_Doc.md) — Internal design of the configuration module.
