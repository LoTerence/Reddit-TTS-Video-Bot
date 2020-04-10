'''
this py file contains all functions main.py needs to work so main isnt so bloated.
for cleaner and more streamlined code
'''
import os, shutil
import re
from PIL import Image
from io import BytesIO

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
    print('Emptied folder: ' + folder)

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
def convertNToK(n):
    k = ''
    if (abs(n > 99999)):
        k = str(int((n - (n % 1000))/1000))+'k'
    elif (abs(n > 999)):
        k = "{0:.1f}".format(n/1000) + 'k'
    else:
        k = str(n)
    return k

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

# Function that turns a list into a list of lists size n
# Yield successive n-sized chunks from l.
# (for moviepy_script.py moviepy bug fix)
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def takeScreenshot(driver, filename):
    bodyElement = driver.find_element_by_id('bodyid')
    location = bodyElement.location
    size = bodyElement.size
    left = location['x']
    top = location['y']
    bottom = location['y'] + size['height'] * 1.3
    im = Image.open(BytesIO(driver.get_screenshot_as_png()))
    im = im.crop((left, top, 950, bottom))  # crop screenshot so we only get the comment / template body
    im.save(filename)  # save screenshot as file

# function for creating an award dict. Param award - award object in prawobject.all_awardings list. Returns dict
def createAward(award):
    award_dict = {}
    award_dict["name"] = award["name"]
    award_dict["count"] = award["count"]
    award_dict["icon"] = award["resized_icons"][1]["url"]  # getting the url of the 32x32 image
    return award_dict

# function for getting all the awardings. Param awardings - list of awardings from praw object. Returns list of award_dicts
def get_awardings(awardings):
    all_awardings = []

    # append platinum, gold and silver awards first:
    for award in awardings:
        if award["name"] == "Platinum":
            all_awardings.append(createAward(award))
            print('Appended ' + award["name"])
            break
    for award in awardings:
        if award["name"] == "Gold":
            all_awardings.append(createAward(award))
            print('Appended ' + award["name"])
            break
    for award in awardings:
        if award["name"] == "Silver":
            all_awardings.append(createAward(award))
            print('Appended ' + award["name"])
            break
    for award in awardings:
        if ((award["name"] == "Platinum") or (award["name"] == "Gold") or (award["name"] == "Silver")):
            print('already added')
        else:
            all_awardings.append(createAward(award))
            print('Appended ' + award["name"])
    return all_awardings