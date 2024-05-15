#!/usr/bin/python3

import os
from filedefines import *
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment

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

data = {}

for main_dir, main_dir_props in dict(table).items():
    dir_path = os.path.join(sounds_path, main_dir)
    data[main_dir] = {}
    print(main_dir)

    for root, _, files in os.walk(dir_path):
        files = sorted(files)
        for file in files:
            name = Path(file).stem
            if ('exclude' in main_dir_props and not name in main_dir_props['exclude']) or 'exclude' not in main_dir_props:
                file_path = os.path.join(root, file)

                output_path = os.path.join(script_dir, "soundpack", main_dir, f"{name}.ogg")
                if file_path.endswith('.wav') and not os.path.exists(output_path):
                    sound = AudioSegment.from_wav(file_path)

                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    sound.export(output_path, format="ogg")
                elif os.path.exists(output_path):
                    data[main_dir][name] = f"{name}.ogg"

tab = "    "
with open(os.path.join(script_dir, "soundpack", "files.lua"), "w") as f:
    f.writelines([
        '--[[\n'
        '———————————No io access?———————————\n',
        '⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝\n',
        '⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇\n',
        '⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀\n',
        '⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀\n',
        '⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀\n',
        '⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀\n',
        '⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀\n',
        '⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀\n',
        '⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n',
        '⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n',
        '⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n',
        '⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n',
        '⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n',
        '—————————————————————————————\n]]\n',
    ])
    f.write("return {\n")
    for folder_name, folder_content in data.items():
        f.write(tab+folder_name+" = {\n")

        for file_name in folder_content:
            f.write(f'{tab*2}["{file_name}"] = "{folder_content[file_name]}",\n')

        f.write(tab+"},\n")
    f.write("}")

mod_base = "hl-soundpack/"
mod_base_translate = "Half-Life/"
with open(os.path.join(script_dir, "locale/en/generated-categories.cfg"), "w") as fcat:
    fcat.write("[programmable-speaker-instrument]\n")

    for cat_name, folder_content in data.items():
        file_base = mod_base+cat_name
        fcat.write(f'{file_base}={mod_base_translate+cat_name}\n')

        file_count = 0
        with open(os.path.join(script_dir, f'locale/en/generated-{cat_name}.cfg'), "w") as fcatsounds:
            fcatsounds.write("[programmable-speaker-note]\n")
            
            for file_name in folder_content:
                file_count += 1
                fcatsounds.write(f'{file_base}/{file_name}=[{file_count}] {file_name}\n')

            print(f'{cat_name} (file count): {str(file_count)}')
