#!/usr/bin/python3

import os
from filedefines import *
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm

# set the directory in the same place as the script
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

# initialize the dictionary
data = {}

for category in fakecategories:
    data[category] = {}

for category, _ in dict(table).items():
    data[category] = {}

# initializing the folder structure
for category in data:
    os.makedirs(os.path.join(script_dir, "soundpack", category), exist_ok=True)

# converting files to a compressed format and moving them to the mod folder
for category, category_props in dict(table).items():
    if category in fakecategories:
        continue

    dir_path = os.path.join(sounds_path, category)
    print(category)

    if 'move' in category_props:
        orig_category_name = category
    else:
        # This is probably not entirely correct, but... I'm going to use this variable in the same way as a flag, then it must be declared
        orig_category_name = False

    for root, _, files in os.walk(dir_path):
        files = sorted(files)
        bar = tqdm(total=len(files), ncols=100, position=0, leave=True)

        for file in files:
            bar.update(1)
            name = Path(file).stem
            if ('exclude' in category_props and not name in category_props['exclude']) or 'exclude' not in category_props:
                if orig_category_name and name in category_props['move']:
                    category = category_props['move'][name]

                file_path = os.path.join(root, file)

                output_path = os.path.join(script_dir, "soundpack", category, f"{name}.ogg")
                if file_path.endswith('.wav') and not os.path.exists(output_path):
                    sound = AudioSegment.from_wav(file_path)

                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    sound.export(output_path, format="ogg")

                if os.path.exists(output_path):
                    data[category][name] = f"{name}.ogg"

                if orig_category_name:
                    category = orig_category_name
        bar.close()

# generating a list of files
tab = "    "
with open(os.path.join(script_dir, "soundpack", "files.lua"), "w") as f:
    f.writelines([
        '--[[\n'
        '———————————No io access?———————————\n',
        '⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝\n',
        '⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇\n',
        '⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏\n',
        '⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁\n',
        '⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉\n',
        '⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂\n',
        '⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂\n',
        '⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁\n',
        '⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏\n',
        '⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝\n',
        '⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟\n',
        '⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟\n',
        '⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋\n',
        '———————————————————————————————————\n]]\n',
    ])
    f.write("return {\n")
    for folder_name, folder_content in data.items():
        f.write(f'{tab}["{folder_name}"] ='+"{\n")

        for file_name in folder_content:
            f.write(f'{tab*2}["{file_name}"] = "{folder_content[file_name]}",\n')

        f.write(tab+"},\n")
    f.write("}")

# localization generation
mod_base = "hl-soundpack/"
mod_base_translate = "Half-Life/"
with open(os.path.join(script_dir, "locale/en/generated-categories.cfg"), "w") as fcat:
    fcat.write("[programmable-speaker-instrument]\n")

    for cat_name, folder_content in data.items():
        file_base = mod_base+cat_name
        fcat.write(f'{file_base}={mod_base_translate+cat_name}\n')

        file_count = 0
        with open(os.path.join(script_dir, f'locale/en/generated-{cat_name.replace('/', '.')}.cfg'), "w") as fcatsounds:
            fcatsounds.write("[programmable-speaker-note]\n")
            
            for file_name in folder_content:
                file_count += 1
                fcatsounds.write(f'{file_base}/{file_name}=[{file_count}] {file_name}\n')

            print(f'{cat_name} (file count): {str(file_count)}')
