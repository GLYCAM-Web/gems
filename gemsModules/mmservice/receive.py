#

##  If this module is receiving a request, then there should be almost no
##  setup required other than whatever is specific to the modeling engine.
##
##  For example, if the modeling engine is amber, then it's ok to have to
##  specify a force field file for building prmtop/inpcrd.  And, it's ok
##  to need to generate an input-control file.  But, there should be no
##  building of coordinates, etc., which aren't really an amber thing.
##  (unless you write modules for using tleap to build, etc.....)
##

def receive(thisTransaction):
    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        pass

def doDefaultService(thisTransaction):
    .setup.check(thisTransaction)
    .amber.md.generate.plainMD(thisTransaction)
    batchcompute.check(thisTransaction)
    batchcompute.generatescript(thisTransaction)
    batchcompute.submit(thisTransaction)

