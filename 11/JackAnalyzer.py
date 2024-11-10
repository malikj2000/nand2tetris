import sys
from os import listdir
from os.path import isfile, isdir, basename
from CompilationEngine import CompilationEngine

def main():
    list_of_files = []
    if isfile(sys.argv[1]):
        list_of_files.append(sys.argv[1])
    elif isdir(sys.argv[1]):
        for file in listdir(sys.argv[1]):
            if file[-5:] == ".jack":
                list_of_files.append(sys.argv[1] + "/" + file)
    
    for file in list_of_files:
        base_name = basename(file)
        output_file = base_name[:-5] + ".xml"
        compilation = CompilationEngine(file, output_file)
        compilation.compileClass()

if __name__ == "__main__":
    main()