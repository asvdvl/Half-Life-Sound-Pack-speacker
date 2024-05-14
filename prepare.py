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
            "# Enter the path to the game core mode. Like $STEAMAPPS_COMMON_PATH/factorio/game/core/\n",
            "CORE_PATH=\n",
        ])

        f.close()
        print("\033[91mNo .env file was found! File has been created, please fill it out.\033[0m")
        exit()

load_dotenv()

sounds_path = os.getenv('SOUNDS_PATH')
CORE_PATH = os.getenv('CORE_PATH')

# Verification that all parameters are filled in:
if not sounds_path or not len(sounds_path) > 0:
    print("\033[91mSOUNDS_PATH in empty.\033[0m")
    exit()

if not CORE_PATH or not len(CORE_PATH) > 0:
    print("\033[91mCORE_PATH in empty.\033[0m")
    exit()

lua = LuaRuntime(unpack_returned_tuples=True)
table = lua.require("file-defines")

data = dict()

for main_dir, main_dir_props in dict(table).items():
    dir_path = os.path.join(sounds_path, main_dir)
    for root, dirs, files in os.walk(dir_path):
        data[main_dir] = dict()
        print(main_dir)
        for file in files:
            name = Path(file).stem
            data[main_dir][name] = file
            file_path = os.path.join(root, file)
            print("-"+name)