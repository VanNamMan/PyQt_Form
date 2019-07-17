import os

from distutils.file_util import copy_file
from distutils.dir_util import copy_tree

files = os.listdir(os.getcwd())
ff = []
for f in files :
    if f[-3:]!=".py" and f[-3:]!=".ui":
        ff.append(f)

print(ff)

if not os.path.exists("Debug"):
    os.mkdir("Debug")
if not os.path.exists("Debug\\build"):
    os.mkdir("Debug\\build")
if not os.path.exists("Debug\\dist"):
    os.mkdir("Debug\\dist")

for f in ff:
    if f == "Debug" or f== "__pycache__":
        pass
    elif os.path.isfile(f):
        copy_file(f,"Debug\\dist\\"+f) # Does bob.txt exist?  Is it a file, or a directory?:
        pass
    elif os.path.isdir(f):
        copy_tree(f,"Debug\\dist\\"+f)
        pass

os.system("pyinstaller -F -w -i res\\bird.ico \
                        --workpath Debug\\build \
                        --specpath Debug\\ \
                        --distpath Debug\\dist \
                        main.py")