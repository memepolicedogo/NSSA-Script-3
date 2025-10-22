#!/bin/python3
import os
import subprocess
import pathlib

HELP = """
    c(reate): Create a shortcut on your desktop
    d(elete): Delete a shortcut from your desktop
    l(ist): List all shortcuts
    h(elp): Print this help message
    q(uit): Exit the program
    """

HOME = str(pathlib.Path.home())

DESKTOP = HOME + "/Desktop/"

def create_shortcut():
    print("Enter a file name")
    file = input()
    proc = subprocess.run(['find', HOME,"-name", file, "-type", "f"], capture_output=True)
    if proc.returncode != 0:
        print("Invalid filename, exiting")
        print(str(proc.stderr))
        return
    out = str(proc.stdout)
    results = out.splitlines()
    if len(results) == 1:
        path = results[0]
        name = path.split("/")[-1]
        print(f"Creating link to {file} at {DESKTOP+name}")
        os.symlink(path, DESKTOP + name)
        return
    print(f"{len(results)} files with the name \"{file}\" found:")
    while(True):
        for i in range(1, len(results)+1):
            print(f"[{i}]\t{results[i-1]}")
        print(f"Which file would you like to use? (1-{len(results)}):")
        print("Enter q(uit) to exit")
        option = input()
        if option.lower()[0] == 'q':
            print("Exiting command")
            return
        try:
            index = int(option)
            if index > len(results):
                raise ValueError
            path = results[index-1]
            name = path.split("/")[-1]
            os.symlink(DESKTOP + str(name), name)
            return
        except ValueError:
            print("Invalid index")



def delete_shortcut():
    print("Enter a shortcut name")
    file = input()
    # find all symlinks on the desktop with the given name
    proc = subprocess.run(['find', DESKTOP,"-name", file, "-type", "l"], capture_output=True)
    if proc.returncode != 0:
        print("Invalid filename")
        return
    out = str(proc.stdout)
    results = out.splitlines()
    if len(results) == 0:
        print(f"No shortcuts named \"{file}\" found:")
        return
    if len(results) == 1:
        print("Deleting shortcut")
        os.unlink(DESKTOP+file)
        return
    print(f"{len(results)} shortcuts with the name \"{file}\" found:")
    while(True):
        for i in range(1, len(results)+1):
            print(f"[{i}]\t{results[i-1]}")
        print(f"Which shortcut would you like to delete? (1-{len(results)}):")
        print("Enter q(uit) to exit")
        option = input()
        if option.lower()[0] == 'q':
            print("Exiting command")
            return 
        try:
            index = int(option)
            if index > len(results):
                raise ValueError
            print("Deleting shortcut")
            os.unlink(DESKTOP+file)
            return
        except ValueError:
            print("Invalid index")




def list_shortcuts():
    # Find shortcuts
    proc = subprocess.run(['find', HOME, "-type", "l"], capture_output=True)
    if proc.returncode != 0:
        print("Something went wrong")
        return
    links = proc.stdout.splitlines()
    for link in links:
        target = os.readlink(link)
        print(f"{link} --> {target}")
    return


print(HELP)
command = ''
while (command != 'q'):
    command = input().lower()[0]
    if command == 'c':
        create_shortcut()
    elif command == 'd':
        delete_shortcut()
    elif command == 'l':
        list_shortcuts()
    else:
        print(HELP)
print("Exiting")

