from sys import argv
from math import ceil
from os import mkdir
from os.path import join

def convert_orthofinder_blast_commands_to_slurm(input_path,output_path,relevant_commands_start_with="diamond blastp"):
    """Convert a file of orthofinder BLAST commands to a slurm file that runs those commands"""
    f = open(input_path)
    commands = []
    for l in f:
        if l.startswith(relevant_commands_start_with):
            commands.append(l)
    return commands

def bundle_commands_into_groups(commands,max_groups = 100):
    """yield commands in groups

    The intent is that this can be used to break commands into a managable number 
    for each slurm script"""

    n_commands = len(commands)
    print(f"Breaking up {n_commands} into equal groups")
    commands_per_group = ceil(n_commands/max_groups)
    print(f"Each group will have ~ {commands_per_group} commands")

    print("Begin yielding command groups...")
    current_command_group = []
    for command in commands:
        if len(current_command_group) >= commands_per_group:
            yield current_command_group
            current_command_group=[]

        current_command_group.append(command)

    #Yield the last command group, even if not maximally full
    yield current_command_group

def make_directory(directory_name):
    try:
        mkdir(directory_name)
        print(f"Directory '{directory_name}' created.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")

def output_command_bundle_to_file(command_bundle,i,output_dir):
    """Write out a BASH script with i as the suffix containing commands"""
    output_filepath = join(output_dir,f"commands_for_slurm_{i}.sh")
    lines = ["#!/bin/bash"+"\n"]
    for command in command_bundle:
        lines.append(command+"\n")
    print("About to write lines:",lines)
    f = open(output_filepath,"w")
    f.writelines(lines)
    f.close()

if __name__ == "__main__":
    input_path = argv[1]
    output_path = argv[2]
    output_dir = join(output_path,"slurm_command_groups")
    make_directory(output_dir)

    
    all_commands = convert_orthofinder_blast_commands_to_slurm(input_path,output_path)
    for i,command_bundle in enumerate(bundle_commands_into_groups(all_commands,max_groups = 128)):
        print(i,f"Bundle of {len(command_bundle)} commands. Example command: {command_bundle[0]}")
        output_command_bundle_to_file(command_bundle,i,output_dir)
    
