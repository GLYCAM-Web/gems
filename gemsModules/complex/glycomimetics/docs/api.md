## Raw dict input 
```json
{
  "entity": {
    "type": "Glycomimetics",
    "services": {
      "step_one_glyco_in_silico": {
        "type": "Build"
      }
    },
    "inputs": {
        # TODO: ComplexPdb -> Resource (others resources too?)
        "ComplexPdb": "3ubq_chainC_64_266.pdbqt",
        # TODO: Also a resource
        "OpenValence": {
            "token1": "328_C5_N5_C10",
            "path": "gemsModules/complex/glycomimetics/metadata/moieties/pdbqt/virtual_screening/sigma_aldehydes",
            "fileType": "pdbqt",
            "token4": "328_C4_C5_N5_H5N"
        },
        # These can be Options resource
        "Interval": 30,
        "NumThreads": 8,
        "OutputPath": "output",
        "LogFile": "sample.log"
    }
  }
}
```

## Resources
```json
{
  "entity": {
    "type": "Glycomimetics",
    "services": {
      "step_one_glyco_in_silico": {
        # TODO: workflow, requesting Analyze actually requests, if necessary:
        # Evaluate -> Validate -> Build -> Analyze
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
        "locationType": "filesystem-path-unix",
        "resourceFormat": "application/json",
        "resourceRole": "moiety-metadata",
        "payload": {
          "token1": "328_C5_N5_C10",
          # will be relative to metadata dir
          "path": "moieties/pdbqt/virtual_screening/sigma_aldehydes",
          "fileType": "pdbqt",
          "token4": "328_C4_C5_N5_H5N"
        }
      },
      {
        "locationType": "filesystem-path-unix",
        "resourceFormat": "application/json",
        "resourceRole": "execution-parameters",
        "payload": {
          "Interval": 30,
          "NumThreads": 8,
          "OutputPath": "output", # Note this will be relative to project dir
          "LogFile": "sample.log"
        }
      }
    ]
  }
}
```

# API Inputs

# JSON Options
