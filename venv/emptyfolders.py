'''
useful script for clearing files in venv
Automatically clears"
/screenshots
/clips
/audio
/jsons
/movie
/submission
'''

import helpfulFuncs as hf

hf.empty_folder(f'artifacts/audio')
hf.empty_folder(f'artifacts/clips')
hf.empty_folder(f'artifacts/jsons')
hf.empty_folder(f'artifacts/movie')
hf.empty_folder(f'artifacts/screenshots')
hf.empty_folder(f'artifacts/submission/audio')
hf.empty_folder(f'artifacts/submission/screenshots')

