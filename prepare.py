#!/usr/bin/python3

import os
from dotenv import load_dotenv
from lupa.lua52 import LuaRuntime
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

env_file = ".env"

if not os.path.exists(env_file):
    with open(env_file, "w") as f:
        f.writelines([
            "# Enter the path to the hl sounds. Like $STEAMAPPS_COMMON_PATH/Half-Life/valve/sound/\n",
            "SOUNDS_PATH=\n",
            "\n",
        ])

        f.close()
        print("\033[91mNo .env file was found! File has been created, please fill it out.\033[0m")
        exit()

load_dotenv()

sounds_path = os.getenv('SOUNDS_PATH')

# Verification that all parameters are filled in:
if not sounds_path or not len(sounds_path) > 0:
    print("\033[91mSOUNDS_PATH in empty.\033[0m")
    exit()

lua = LuaRuntime(unpack_returned_tuples=True)
table = lua.require("file-defines")

data = {}

for main_dir, main_dir_props in dict(table).items():
    dir_path = os.path.join(sounds_path, main_dir)
    data[main_dir] = {}
    file_count = 0
    print(main_dir, end="")
    for root, _, files in os.walk(dir_path):
        for file in files:
            name = Path(file).stem
            data[main_dir][name] = file
            file_path = os.path.join(root, file)
            file_count += 1
    print(" (file count): "+str(file_count))

tab = "    "
with open(os.path.join(script_dir, "soundpack", "files.lua"), "w") as f:
    f.write("return {\n")
    for folder_name, folder_content in data.items():
        f.write(tab+folder_name+" = {\n")

        for file_name in folder_content:
            f.write(tab*2+'"'+file_name+'",\n')

        f.write(tab+"}\n")
    f.write("}")
    
