'''
this py file contains all functions main.py needs to work so main isnt so bloated.
for cleaner and more streamlined code
'''
import os, shutil
import re

# dictionary for bad and weird words and their replacements:
# also replaces program breaking words like <br> etc
bad_words = {
    'fuck':' duck',
    'shitty':'crappy',
    'shit': 'crap',
    'bitch':'beach',
    'isnt':'isn\'t',
    '<br>':' ',
    '--':' ',
    '*':' ',
    '\"':' '
}

# compiles the punctuation into one regex object: punctuation_regex (for parsing sentences in comment.body)
punctuation_regex = re.compile('(?<=[\n.!,?:;])+')

# function that empties contents of a folder. Returns nothing
def empty_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

#function for removing emojis from a string
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

# function for removing links from a str (for removing links from comment.body
def deLinkify(s):
    temp = re.sub(r'\(https?://\S+', '', s)
    temp = re.sub(r'https?://\S+', '', temp)
    return temp

#convert score to 'x.x k' if score is over 999
#takes int and returns str
def convertKarmaToK(score):
    karma = ''
    if (abs(score > 999)):
        karma = "{0:.1f}".format(score/1000) + 'k'
    else:
        karma = str(score)
    return karma

#replace \n with <br>
def convertLnToBr(s):
    part =''
    if '\n' in s:
        part = s.replace('\n', '<br>')
    else:
        part=s
    return part

def cleanSpeech(s):
    speech = s
    for key, value in bad_words.items():
        if key in speech:
            speech = speech.replace(key, value)
    return speech

