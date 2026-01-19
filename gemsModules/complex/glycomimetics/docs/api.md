# GM Request using input Resources
```json
{
  "entity": {
    "type": "Glycomimetics",
    "services": {
      "simple_glycomimetics_request": {
        # TODO: eventual workflow, requesting Analyze actually requests, if necessary:
        # Evaluate -> Validate -> ProjectManagement -> Build -> Analyze is implied.
        "type": "Analyze"
        # Analyze implies Build, and the below input Resources will be copied by Build's implied translator.
      }
    },
    # These inputs are primarily for Build, however, Evaluate and Validate will check them.
    # Analyze will use the outputs of Build, likely interacting with resources from Build.
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

### API Inputs

### JSON Options

# Workflow

[workflow.md](workflow.md)