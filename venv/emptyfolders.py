'''
useful script for clearing files in venv
Automatically clears"
/screenshots
/clips
/audio
/title
/movie
'''

import helpfulFuncs as hf

hf.empty_folder(f'artifacts/audio')
hf.empty_folder(f'artifacts/clips')
hf.empty_folder(f'artifacts/screenshots')
hf.empty_folder(f'artifacts/title')
hf.empty_folder(f'artifacts/movie')