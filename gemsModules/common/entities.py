#!/usr/bin/env python3

## The module to load for each Entity type
entityModule = {
  'Delegator'         : 'delegator' ,
  'Sequence'          : 'sequence' ,
  'Glycoprotein'      : 'glycoprotein'
}
## The name of the text to return for various types of help
helpDict = {
  'ReturnUsage'       : 'usageText',
  'ReturnHelp'        : 'basicHelpText',
  'ReturnVerboseHelp' : 'moreHelpText',
  'ReturnSchema'      : 'schemaLocation'
}

def main():
    print("Ths script only contains dictionary information about Entities.")

if __name__ == "__main__":
  main()

