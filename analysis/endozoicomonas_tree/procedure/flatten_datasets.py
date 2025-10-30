from sys import argv
from os import listdir,rename
from os.path import join,exists

def flatten_ncbi_files(target_dir,flat_dir):

    ncbi_files = listdir(join(target_dir,"data"))
    print(ncbi_files)

    for subdir in ncbi_files:
        if 'json' in subdir:
            print(f"Skipping subdir {subdir}")
            continue
        starting_path = join(target_dir,"data",subdir,"protein.faa")
        print(f"Moving file at starting path {starting_path}")
        ending_path = join(flat_dir,f"{subdir}.faa")
        print(f"Moving file to new path: {ending_path}")
        if not exists(starting_path):
            print(f"Skipping move of {starting_path}....file doesn't exist")
            continue
        rename(starting_path,ending_path)

if __name__ == "__main__":
    flatten_ncbi_files(argv[1],argv[2])    
