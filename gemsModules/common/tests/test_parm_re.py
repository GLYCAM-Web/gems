import re

def parse_amber_parm7_natoms(content):
    #  Match the entire POINTERS section, extracting the format string and data
    pointers_regex = re.compile(r'%FLAG POINTERS\s*\n%FORMAT\s*\((\d+[Ii]\d+)\)\s*(.*?)(?=\n%FLAG|\Z)', re.DOTALL)
    
    match = pointers_regex.search(content)
    if not match:
        raise ValueError("POINTERS section not found in the content")
    
    format_str, data_str = match.groups()
    
    # Parse the format string
    num_per_line, char_per_num = map(int, re.findall(r'\d+', format_str))
    
    # Remove newlines and extra spaces, then split the data
    data_str = data_str.replace('\n', '').strip()
    data = [data_str[i:i+char_per_num].strip() for i in range(0, len(data_str), char_per_num)]
    
    
    # Convert to integers
    pointers = list(map(int, data))
    
    # NATOMS is the first value in the POINTERS section
    natoms = pointers[0]
    
    return natoms

# Example usage
example_content = """
%VERSION  VERSION_STAMP = V0001.000  DATE = 04/18/23  03:59:31                  
%FLAG TITLE                                                                     
%FORMAT(20a4)                                                                   
Cpptraj                                                                         
%FLAG POINTERS                                                                  
%FORMAT(10I8)                                                                   
1000107111111118    1059      12      25      17      45      33       0       0
    1529     351      12      17      33       8      13      18       8       1
       0       0       0       0       0       0       0       2      22       0
       0
%FLAG ATOM_NAME                                                                 
%FORMAT(20a4)                                                                   
HO1 O1  C1  H1  C2  H2  C3  H3  C4  H4  C5  H5  C6  H62 H61 O6  H6O O5  O4  H4O 
"""

try:
    natoms = parse_amber_parm7_natoms(example_content)
    print(f"NATOMS: {natoms}")
except ValueError as e:
    print(f"Error: {e}")