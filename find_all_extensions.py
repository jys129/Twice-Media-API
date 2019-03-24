from pathlib import Path
import os

# Not used in the actual program
# A quick script to recursively find all the file extension
# types in a directory (and all of it's subdirectories)


file_extensions = []

for root, dirs, files in os.walk(os.getcwd(), topdown=False):
   for name in files:
        filepath = os.path.join(root, name)
        print(filepath)
        filename, file_extension = os.path.splitext(filepath)    
        
        if file_extension not in file_extensions:
            file_extensions.append(file_extension)    

print(file_extensions)
