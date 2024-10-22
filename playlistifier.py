import os
import sys

def listChildFiles(path, is_root_path = False):
    # Recursively find all files and dirs that are needed for playlist creation
    try:
        children_list = os.listdir(path)
    except:
        print(f"WARNING: Couldn't read \"{path}\"")
        return

    if len(children_list) == 0:
        print(f"No children found in {path}! Returning from branch!")
        return 

    for child_path in children_list:
        child_path = os.path.join(path, child_path)

        # Check ignore list for matches
        ignoreTriggered = False
        for ignore in ignore_list:
            if ignore in child_path:
                ignoreTriggered = True

        if ignoreTriggered:
            print(f"Ignored \"{child_path}\"")
            continue

        elif os.path.isdir(child_path):
            print(f"Branching into \"{child_path}\"")
            listChildFiles(child_path)

        elif not is_root_path and os.path.isfile(child_path) and (child_path.endswith(".mp3") or child_path.endswith(".flac")):
            print(f"Added \"{child_path}\" to playlist")
            files.append(child_path)

        else:
            print(f"Ignored \"{child_path}\"")
            continue

print(" ~ Made by exosZoldyck ~ ")

# Parse args
root_dir_path = "./"
if len(sys.argv) <= 1:
    root_dir_path = input("WARNING: Root directory path was not defined in args!\nInput root directory: ").replace("\"", "")
else:
    root_dir_path = sys.argv[1]

print(f"\nRoot directory path: \"{root_dir_path}\"")

# Check for ignores in ignore.txt
ignore_list = []
ignore_file_path = os.path.abspath("./ignore.txt")
if os.path.isfile(ignore_file_path):
    try:
        file_reader = open(ignore_file_path, "r", encoding="utf-8")
        ignore_string = file_reader.read()
        ignore_list = ignore_string.splitlines()
        
        if len(ignore_list) <= 0:
            print("\nNo ignores provided.")
        else:
            print("\nIgnore list:")
            for ignore in ignore_list:
                print(ignore)
            print("")
    except:
        print("\nWARNING: Couldn't read \"ignore.txt\" file!")
else: 
    print("\nNo \"ignore.txt\" file detected.")

files = [] # Tree of subfiles and subdirs of root dir

if not(os.path.exists(root_dir_path)) or not(os.path.isdir(root_dir_path)):
    print("Error: Root directory does not exist!")
    exit()  

# Define root dir absolute path and start child search
root_dir_path = os.path.abspath(root_dir_path)
listChildFiles(root_dir_path, True) 

# Turn absolute file path into relative
files_relative = []
for file in files:
    file_relative = os.path.relpath(file, root_dir_path)
    file_relative = file_relative.replace("\\", "/")
    files_relative.append(file_relative)
files = files_relative

print("")
for file in files:
    print(f"{file}")
print("")

# Create list of playlist names from first root dir child dir names
playlist_names = []
for file in files:
    if "/" not in file:
        continue
    
    playlist_name = file.split('/')[0]

    if playlist_name not in playlist_names:
        playlist_names.append(playlist_name)

# Start creating playlists and writing playlist files
overwrite_all_files = False
playlists_created = []
for playlist_name in playlist_names:
    print(f"Creating playlist \"{playlist_name}\"")

    # Create and sort playlist array
    playlist = []

    for file in files:
        if file.startswith(playlist_name):
            playlist.append(file)

    if (len(playlist) == 0):
        continue

    playlist.sort()

    print(f"{playlist_name}:")
    for file in playlist:
        print(f" --> {file}")

    playlist_abspath = os.path.abspath(os.path.join(root_dir_path, playlist_name)).replace("\\", "/")
    if os.path.isdir(playlist_abspath):
        playlist_file_path = f"{playlist_abspath}/{playlist_name}.m3u"
        
        # Check for existing playlist files and overwrite after prompt
        if not os.path.isfile(playlist_file_path): 
            try:
                file_writer = open(playlist_file_path, "x")
                file_writer.close()
            except:
                input("Error: Could not write playlist file!")
                exit()
        else:
            if not overwrite_all_files:
                print(f"\nWARNING: Overwriting existing file \"{playlist_file_path}\"!")
                print("Please confirm overwrite by typing \"yes\" for just this case or \"all\" for all future cases: ")
                overwrite_prompt = input("Overwrite? ")
                overwrite_prompt = "" + overwrite_prompt.lower()

            if overwrite_prompt == "all":
                overwrite_all_files = True
            
            if not overwrite_all_files and overwrite_prompt != "yes" and overwrite_prompt != "y":
                continue

            try:
                os.remove(playlist_file_path)
                file_writer = open(playlist_file_path, "x")
                file_writer.close()
            except:
                input("Error: Could not write playlist file!")
                exit()

        # Write playlist files
        try:
            file_writer = open(playlist_file_path, "a", encoding="utf-8")
            for file in playlist:
                    file = f"./{file[file.find('/') + 1:len(file)]}"
                    file_writer.write(f"{file}\n")
            file_writer.close()
        except:
            input("Error: Could not write playlist file!")
            exit()

        print(f"Successfully created playlist file \"{playlist_file_path}\"\n")
        playlists_created.append(playlist_name)
    else:
        print(f"Error: Unable to write file! Directory \"{playlist_abspath}\" does not exist!")

# Write list of created playlists
if len(playlists_created) > 0: 
    print("Playlist created:")
else:
    print("No playlists created!")
for playlist_name in playlists_created:
    print(playlist_name)

input("\nDone!")
exit()