from gemsModules.deprecated.sequence.build import buildEach3DStructureInStructureInfo
if GEMS_FORCE_SERIAL_EXECUTION == 'True':
    buildEach3DStructureInStructureInfo(self)
else:
    from gemsModules.deprecated.common import logic as commonlogic
    def buildArgs() : # This merely simplifies the multiprocessing.Process call below
        buildEach3DStructureInStructureInfo(self)
    import multiprocessing
    detachedBuild=multiprocessing.Process(target=commonlogic.spawnDaemon, args=(buildArgs,))
    detachedBuild.daemon=False
    detachedBuild.start()

