import gemsModules
from gemsModules import common
from gemsModules.common import resources

thisResource = resources.Resource()
thisResource.notices.addDefaultNotice(Brief='GemsError')
print("""
        """)
thisResource.notices.printNotices(style='terse',sendTo='stdout')  ### this was put in for the purpose of simplifying testng
print("""
        """)
print(str(thisResource.json(indent=2)))
