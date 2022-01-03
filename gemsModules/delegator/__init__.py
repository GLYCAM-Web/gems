"""
This is the receptionist for the gemsModules.  

Generally, a request will come to the delegator in the 
form of a JSON object.  The delegator will then try to
figure out which other gemsModule should handle the request.
If it can't figure this out, it will usually return a
useful statement about why.
"""
#from . import receive, helpme, settings
