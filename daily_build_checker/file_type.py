import magic

def get_file_type(file):
        
      """This function returns the file type and MIME
            type of the file, by testing against custom
            libmagic database files made for the files we 
            generate."""
      mag_obj = magic.Magic(magic_file = "pdb_magic")
      return(mag_obj.from_file(file))


        
        
        

        

        


