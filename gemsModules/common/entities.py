#!/usr/bin/env python3

## Let python know that these things exist.
## They will be redefined elsewhere.
#def delegator():
  #pass
#def sequence():
  #pass
#def glycoprotein():
  #pass


entityFunction = {
  'Delegator'         : 'delegator' ,
  'Sequence'          : 'sequence' ,
  'Glycoprotein'      : 'glycoprotein'
}
helpDict = {
  'Usage'     : 'usageText',
  'Help'      : 'basicHelpText',
  'More Help' : 'moreHelpText',
  'Schema'    : 'schemaLocation'
}

def main():
    print("Ths script only contains dictionary information about Entities.")

if __name__ == "__main__":
  main()

