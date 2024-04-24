## GM Request using input Resources
```json
{
  "entity": {
    "type": "Glycomimetics",
    "services": {
      "step_one_glyco_in_silico": {
        # TODO: eventual workflow, requesting Analyze actually requests, if necessary:
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

# API Inputs

# JSON Options
