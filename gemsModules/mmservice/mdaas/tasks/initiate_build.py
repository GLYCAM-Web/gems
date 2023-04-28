from gemsModules.mmservice.mdaas.tasks import amber_submisison

def execute(use_serial : bool = False, pUUID : str, outputDirPath: str, control_script : str = "Run_Protocol.bash"):

    if use_serial == True:
        amber_submisison.execute(pUUID=pUUID, outputDirPath=outputDirPath, control_script=control_script)
    else:
        from gemsModules.deprecated.common import logic as commonlogic
        def buildArgs() : # This merely simplifies the multiprocessing.Process call below
            amber_submisison.execute(pUUID=pUUID, outputDirPath=outputDirPath, control_script=control_script)
        import multiprocessing
        detachedBuild=multiprocessing.Process(target=commonlogic.spawnDaemon, args=(buildArgs,))
        detachedBuild.daemon=False
        detachedBuild.start()

