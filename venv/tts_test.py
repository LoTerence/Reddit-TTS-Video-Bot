"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="misc/google/My Project 5605-5bd898580668.json"

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.types.VoiceSelectionParams(
    language_code = 'en-US',
    ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3
)

# Set the text input to be synthesized
# Replace this with the title of the post
synthesis_input = texttospeech.types.SynthesisInput(
    text = "this is a smiling Kanye, it only appears once every twenty thousand kanye pics, very rare kanye. Like in five seconds or bad luck.")



# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(synthesis_input, voice, audio_config)


# The response's audio_content is binary. 
with open('misc/kanye-like-or.mp3', 'wb') as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "misc/kanye-like-or.mp3"')

'''
with open('voice_fix.mp3', 'wb') as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "voice_fix.mp3"')
'''