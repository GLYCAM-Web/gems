This is a place to store all the random little things that need doing.  Some are small and simple.  Some are larger and require design.   Please be as specific as possible

I expect this card to never go out of focus.  Remove items from the list once they are done, or once they become obsolete.  Add more whenever you come across them.  

Some of these might be great things to give new folks.

- [ ] In `common/main_api.py` in the class CommonAPI, either define some options to put into the 'options' in the model or get rid of it.  
	- [ ] Check to see if any entities or services use those options.
	- [ ] If it is to be kept, then add code for moving the options set at that level closer to whatever part of the code actually uses the option(s).
- [ ] Change name of 'logger' module so that it doesn't clash with other names in Python space
- [ ] Periodically do a sweep to ensure no collisions with common Python libraries
- [ ] (ABC, BaseModel) or (BaseModel, ABC)?
- [ ] Make it easier for Entities to use services defined in Common.  Right now, my (BLF) hack will make each Entity have to define, import, etc., each service from Common.  If there is time, i will fix this, but it's not an onerous task at the moment to copy-paste the few from Common that probably won't need mods.
- [ ] Naming consistency... namingConsistency... naming_consistency... my_Naming_Consistency...
- [ ] make `__repr__` methods for all these specialized objects
- [ ] 