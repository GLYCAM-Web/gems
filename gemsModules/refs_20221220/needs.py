#/she/bang/python3

# This should hold various stuff needed by the project module,
# including list of things to do and sample code, etc.

# This code needs to:
#  
# 1. Figure out if there is a set path for output/input.  If not set a default.
# 2. Decide if any directories need to be created.  Create them.
# 3. Figure out if any files need to be put into or read from anywhere.
# 4. Deposit needed files into the directories.  Read files as needed.
# 5. Record info wherever it needs recording (Project? Resource?)

The following is from here:  https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python
>>> import uuid
>>> uuid.uuid4()
UUID('bd65600d-8669-4903-8a14-af88203add38')
>>> str(uuid.uuid4())
'f50ec0b7-f960-400d-91f0-c42a6d44e3d0'
>>> uuid.uuid4().hex
'9fe2c4e93f654fdbb24c02b15259716c'
