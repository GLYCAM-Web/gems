from gemsModules.structureFile.amber import io as amberIO
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def preprocessPdbForAmber(receivedTransaction : amberIO.PdbTransaction):
    log.info("preprocessPdbForAmber() was called. Still in Development!!!!!!!!")

    # ## Grab the input
    # try:
    #     uploadFile = getPdbFileFromTransaction(receivedTransaction)
    # except Exception as error:
    #     log.error("There was a problem getting the pdbFile from the transaction: " + str(error))
    #     log.error(traceback.format_exc())
    #     raise error



    ##TODO: write the logic to evaluate, and then write the processed pdb out to file.

    ## Keep this stuff for a reference, but replace it with better stuff. 
    ##VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
    #output = amberIO.PreprocessPdbForAmberOutput()
    # try:
    #     pdbFile = generatePdbFile(receivedTransaction)
    #     log.debug("pdbFile output: " + str(pdbFile))
    # except Exception as error:
    #     log.error("There was a problem generating the PDB output.")
    #     raise error
    # else:

    #     ### Write the content to file
    #     try:
    #         writePdbOutput(receivedTransaction, pdbFile)
    #     except Exception as error:
    #         log.error("There was a problem writing the pdb output." + str(error))
    #         raise error

    ##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^