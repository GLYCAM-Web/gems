import magic

def get_mime_type(file):
        
      """This function returns the MIME type of a file"""

      mime_type = magic.from_file(file, mime=True)

      if mime_type:
            return(mime_type)
      else:
            return("Unknown MIME Type")

        
        
        

        

        


