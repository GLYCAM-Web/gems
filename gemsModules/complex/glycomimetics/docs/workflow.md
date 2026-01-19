## Request a Glycomimetics Analysis

```json
{
  "entity": {
    "type": "Glycomimetics",
    "services": {
      "step_one_glyco_in_silico": {
        # TODO: workflow, requesting Analyze actually requests, if necessary:
        # Evaluate -> Validate -> Build -> Analyze is implied.
        "type": "Analyze"
      }
    },
    "inputs": [
      {
        "locationType": "filesystem-path-unix",
        "resourceFormat": "chemical/pdbqt",
        "resourceRole": "cocomplex-input",
        "payload": "3ubq_chainC_64_266.pdbqt"
      },
      {
        "locationType": "Payload",
        "resourceFormat": "application/json",
        "resourceRole": "moiety-metadata",
        "payload": {
          "token1": "328_C5_N5_C10",
          # Note this will be relative to metadata dir
          "path": "moieties/pdbqt/virtual_screening/sigma_aldehydes",
          "fileType": "pdbqt",
          "token4": "328_C4_C5_N5_H5N"
        }
      },
      {
        "locationType": "Payload",
        "resourceFormat": "application/json",
        "resourceRole": "execution-parameters",
        "payload": {
          "Interval": 30,
          "NumThreads": 8,
           # Note this will be relative to project dir (PM service)
          "OutputPath": "output",
          "LogFile": "sample.log"
        }
      }
    ]
  }
}
```

The above inputs and service will imply a workflow of Evaluate -> Validate -> Build -> Analyze.

These inputs are destined primarily for the Build service, but the Evaluate and Validate services both need to be aware of the inputs to ensure that the Build service can proceed. The Analyze service uses outputs from the Build service. 

--- 

Internally, the first step will be to separate the cocomplex into receptor and ligand:
- The receptor will be saved as a PDB file, and the ligand will be saved as a PDB file. 
- The matching results will be saved as a text file.

The payload paths will be relative to the project directory and handled by the ProjectManagement service.

## STEP_1_INTERMEDIATE_OUTPUT_RESOURCES

```json
 [
    {
        "locationType": "filesystem-path-unix",
        "resourceFormat": "chemical/pdb",
        "resourceRole": "receptor",
        "payload": "3ubq_chainC_64_266.pdb"
    },
    {
        "locationType": "filesystem-path-unix",
        "resourceFormat": "chemical/pdb",
        "resourceRole": "ligand",
        "payload": "3ubq_chainC_64_266.pdb"
    },
    {
        "locationType": "filesystem-path-unix",
        "resourceFormat": "text",
        "resourceRole": "matching-results",
        "payload": "3ubq_chainC_64_266.txt"
    }
 ]
 ```