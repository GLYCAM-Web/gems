import re 

with open("Galactose.pdb") as f:
    contents = f.read()

pattern = re.compile("^ATOM")
pattern_2 = re.compile("x")

print(pattern.search(contents))
print(pattern_2.search(contents))
