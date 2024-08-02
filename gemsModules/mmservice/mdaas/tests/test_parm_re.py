import re
import logging 

from gemsModules.mmservice.mdaas.tasks.calculate_days_per_ns import parse_amber_parm7_natoms, parse_amber_parm7_pointers

logging.basicConfig(level=logging.DEBUG)
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

bugged_content = """
%FLAG POINTERS                                                                  
%FORMAT(10I8)                                                                   
     456      11     214     258     487     385     881     676       0       0
    2694      18     258     385     676      18      39      39      14       0
       0       0       0       0       0       0       0       0      37       0
       0
%FLAG ATOM_NAME                                                                 
%FORMAT(20a4)    
"""
test_path = None
# test_path = "/programs/gems/tests/temp-inputs/mdinput/DGlcpa1-OH.parm7"
# test_path = "/programs/gems/tests/correct_outputs/008_reference/cb_final_state/Builds/19b670a1-5621-415a-a708-537ce0fe5491/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39/unminimized-gas.parm7"
try:
    pointers = parse_amber_parm7_pointers(bugged_content)
    print(f"POINTERS: {pointers}")
except ValueError as e:
    print(f"Error: {e}")


if test_path:
    try:
        natoms = parse_amber_parm7_natoms(test_path)
        print(f"NATOMS: {natoms}")
    except ValueError as e:
        print(f"Error: {e}")