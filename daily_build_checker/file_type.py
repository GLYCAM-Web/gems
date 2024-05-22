import re

def is_PDB(file):
        
      """This function using regex to identify PDB files."""
      with open(file) as f:
            contents = f.read()

      pdb_regex = re.compile("ATOM\s*[0-9]*\s\s")

      if pdb_regex.search(contents) != None:
            return("PDB file")
      
      else:
            return("This is not a PDB file")
            
      
        
        
        

        

        


