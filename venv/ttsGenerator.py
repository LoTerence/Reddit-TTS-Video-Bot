'''
ttsGenerator.py

for housing the tts audio generatoring parts of main.py
'''
from google.cloud import texttospeech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="misc/google/My Project 5605-5bd898580668.json"

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
voice = texttospeech.types.VoiceSelectionParams(  # set language and gender of voice
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
audio_config = texttospeech.types.AudioConfig(  # set audio file type to mp3
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

# function for generating tts. Takes any string as s. Returns nothing. Saves tts to string filename
def gen_tts(s, filename):
    synthesis_input = texttospeech.types.SynthesisInput(text=s)  # set the text to be synthesized
    audio_res = client.synthesize_speech(synthesis_input, voice, audio_config)  # generate speech and save to variable audio_res
    with open(filename, 'wb') as out:
        # Write the response to the output file.
        out.write(audio_res.audio_content)  # save to mp3 file in audio folder
        print('Title Audio content written to file ' + filename)