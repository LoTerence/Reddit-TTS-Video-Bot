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

# function that takes a str and creates an mp3 file representing its TTS. Returns str audio_filename
def generate_tts(s, comment_i, sentence_i):
    synthesis_input = texttospeech.types.SynthesisInput(text=s)  #set the text to be synthesized
    audio_res = client.synthesize_speech(synthesis_input, voice, audio_config)  #generate speech and save to variable audio_res
    audio_filename = 'artifacts/audio/voice_' + str(comment_i) + '_' + str(sentence_i) + '.mp3'
    with open(audio_filename, 'wb') as out:
        # Write the response to the output file.
        out.write(audio_res.audio_content)   # save to mp3 file in audio folder
        print('Audio content written to file '+ audio_filename)
    return audio_filename

# function for generating title tts. Takes post title as param s. Returns nothing. Saves tts to title/title_tts.mp3
def gen_title_tts(s):
    synthesis_input = texttospeech.types.SynthesisInput(text=s)  # set the text to be synthesized
    audio_res = client.synthesize_speech(synthesis_input, voice, audio_config)  # generate speech and save to variable audio_res
    audio_filename = 'artifacts/title/title_tts.mp3'
    with open(audio_filename, 'wb') as out:
        # Write the response to the output file.
        out.write(audio_res.audio_content)  # save to mp3 file in audio folder
        print('Title Audio content written to file ' + audio_filename)
