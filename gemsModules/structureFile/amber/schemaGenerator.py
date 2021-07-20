#!/usr/bin/env python3
import os, sys, importlib.util
import pathlib
import traceback
import gemsModules.structureFile.amber.io as amberIO
# from gemsModules.common.loggingConfig import *
# from gemsModules.common import io as commonio
# from gemsModules.common.logic import updateResponse, getGemsHome


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

# 1) Define one structure for each type of record.
## UnrecognizedAtom ##
## UnrecognizedMolecule ##
## MissingResidue ##
## HistidineProtonation ##
## DisulfideBond ##
## ChainTermination ##
## ReplacedHydrogen ##

# 2) Provide table metadata for things like labels.

##  @brief Build the data needed for the pdb options tables.
##  @detail Use classes in io.py to generate schema that will be used to build models.py. 
##          Primarily for use by the pdb app in the website.
def generateStructureFileSchemaForWeb():
    log.info("generateStructureFileSchemaForWeb() was called.")
    schema = {}
    try:
        ## unrecognizedAtom ##
        unrecognizedAtomsTableMetadataSchema = amberIO.generateUnrecognizedAtomsTableMetadataSchema()
        log.debug("unrecognizedAtomsTableMetadataSchema: \n" + str(unrecognizedAtomsTableMetadataSchema))
        unrecognizedAtomSchema = amberIO.generateUnrecognizedAtomSchema()
        log.debug("unrecognizedAtomSchema: \n" + str(unrecognizedAtomSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})

        ## unrecognizedMolecule ##
        unrecognizedMoleculesTableMetadata = amberIO.generateUnrecognizedMoleculesTableMetadataSchema()
        log.debug("unrecognizedMoleculesTableMetadata: " + str(unrecognizedMoleculesTableMetadata))
        unrecognizedMoleculeSchema = amberIO.generateUnrecognizedMoleculeSchema()
        log.debug("unrecognizedMoleculeSchema: " + str(unrecognizedMoleculeSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})        

        ## missingResidue ##
        missingResiduesTableMetadataSchema = amberIO.generateMissingResiduesTableMetadataSchema()
        log.debug("missingResiduesTableMetadataSchema: \n" + str(missingResiduesTableMetadataSchema))
        missingResidueSchema = amberIO.generateMissingResidueSchema()
        log.debug("missingResidueSchema: \n" + str(missingResidueSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})    
        
        ## histidineProtonation ##
        histidineProtonationsTableMetadataSchema = amberIO.generateHistidineProtonationsTableMetadataSchema()
        log.debug("histidineProtonationsTableMetadataSchema: \n" + str(histidineProtonationsTableMetadataSchema))
        histidineProtonationSchema = amberIO.generateHistidineProtonationSchema()
        log.debug("histidineProtonationSchema: \n" + str(histidineProtonationSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})
        
        ## disulfideBond ##
        disulfideBondsTableMetadataSchema = amberIO.generateDisulfideBondsTableMetadataSchema()
        log.debug("disulfideBondsTableMetadataSchema: \n" + str(disulfideBondsTableMetadataSchema))
        disulfideBondSchema = amberIO.generateDisulfideBondSchema()
        log.debug("disulfideBondSchema: \n" + str(disulfideBondSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})
        
        ## chainTermination ##
        chainTerminationsTableMetadataSchema = amberIO.generateChainTerminationsTableMetadataSchema()
        log.debug("chainTerminationsTableMetadataSchema: \n" + str(chainTerminationsTableMetadataSchema))
        chainTerminationSchema = amberIO.generateChainTerminationSchema()
        log.debug("chainTerminationSchema: \n" + str(chainTerminationSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})
        
        ## replacedHydrogen ##
        replacedHydrogensTableMetadataSchema = amberIO.generateReplacedHydrogensTableMetadataSchema()
        log.debug("replacedHydrogensTableMetadataSchema: \n" + str(replacedHydrogensTableMetadataSchema))
        replacedHydrogenSchema = amberIO.generateReplacedHydrogenSchema()
        log.debug("replacedHydrogenSchema: \n" + str(replacedHydrogenSchema))
        schema.update({"unrecognizedAtom": {
            "unrecognizedAtomsTableMetadataSchema" : unrecognizedAtomsTableMetadataSchema,
            "unrecognizedAtomSchema": unrecognizedAtomSchema
        }})
         
    except Exception as error:
        log.error("There was a problem generating the schema for the structureFile gemsModule: " + str(error))
        log.error(traceback.format_exc())
        raise error

    if schema == {}:
        log.error("There was a problem writing the schema to file.")
    else:
        log.debug("Writing schema to file.")
        file = os.path.join(getGemsHome(), "gemsModules", "Schema", 'pdbOptionsSchema.json')
        log.debug("file: " + file)


if __name__ == "__main__":
    generateStructureFileSchemaForWeb()
