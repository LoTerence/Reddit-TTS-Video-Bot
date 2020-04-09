'''
reddit tts youtube bot for automating askreddit thread youtube video creation
written by Terence Lo
'''
from string import Template
from selenium import webdriver
from PIL import Image
from io import BytesIO
import json
import helpfulFuncs as hf
import ttsGenerator as ttsg


# first thing I have to do: Empty [audio, screenshots, title?, clips] folders of old content
hf.empty_folder(f'artifacts/audio')
hf.empty_folder(f'artifacts/clips')
hf.empty_folder(f'artifacts/screenshots')


# Read comment_body_list json and save to variable comments_list
comment_body_list = []
with open('artifacts/title/comment_bodies.json', 'r') as filehandle:
    comment_body_list = json.load(filehandle)
filehandle.close()


#prepare comment templates
f = open("html_templates/reddit-comment.html","r")
comment_template = Template(f.read())
f.close()
f = open("html_templates/reddit-comment-noheight.html","r")
comment_template_h = Template(f.read())
f.close()


#make a value for the comment iterator:
comment_i = 0 #comment index


#make a list of comments that will contain lists representing the sentences of each comment
# [ comment0[ sentence0[ screenshot0, audio0 ], s1[ sc1, a1 ], s2[ sc2, a2 ] ... ]
#   c1[ s0[ sc0, a0 ], ...]
#   c2....
# ]
# the screenshot and audio are strings of the screenshot and audio's file name
# this will be saved to a json format so that it can be used by moviepy script later
comments_list = []   #as we loop through comments, we add its list of sents (screenshots + audio) to this list


# instantiate selenium webdriver object (for screenshots later)
driver = webdriver.Chrome()
driver.fullscreen_window()


#loop through top n comments and split into sentences
for comment in comment_body_list:

    #get the height of the comment text area
    comment_temp = comment['body']  # save content of comment['body'] to temporary str var
    comment_temp = hf.convertLnToBr(comment_temp)
    sub = comment_template_h.substitute(username=comment['author'], commentbody=comment_temp)  # write comment content into noheight template
    f = open('html_templates/r_comment.html', 'w') # open blank file for writing reddit comment html
    f.write(sub)  # write the html template with the comment data substituted in
    f.close()
    driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/r_comment.html')
    comment_height = driver.find_element_by_id("comment").size["height"] +2  #get the height of comment text area


    # Split the comment into sentences
    #split comment body into a list of sentences seperated by punctuation
    comment_temp = comment['body']
    sentences = list(filter(None, hf.punctuation_regex.split(comment_temp)))
    print(sentences)  #test if I got the sentences right

    # karma - convert comment['score'] to k's if over 999, else keep it the same
    karma = hf.convertNToK(comment['score'])

    commentBodySub = ''  # make value for comment body substitute, as we loop through sentences we append sentences to commentBodySub

    sentence_i = 0 #sentence index per comment

    # sentence list: will contain lists representing the screenshot and audio
    # this will then be added to comment_list at the end of the sentences loop
    sentences_list = []

    for sentence in sentences:

        #replace newlines in sentence with <br>
        sentence = hf.convertLnToBr(sentence)

        commentBodySub+=sentence #append sentence to comment body for the template

        # create html files with the template using individual sentences
        sub = comment_template.substitute(username=comment['author'], karma=karma,
                                          awards=' ', px=str(comment_height)+'px', commentbody=commentBodySub)

        #open blank file for writing reddit comment html
        f = open('html_templates/r_comment.html', 'w')
        f.write(sub) #write the html template with the comment data substituted in
        f.close() #save the write

        # take screenshot of reddit comment and save to screenshots folder
        driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/r_comment.html')  #open the html template in selenium webdriver

        #save screenshot in screenshots folder
        bodyElement = driver.find_element_by_id('bodyid')
        location = bodyElement.location
        size = bodyElement.size
        left = location['x']
        top = location['y']
        bottom = location['y'] + size['height'] * 1.3
        im = Image.open(BytesIO(driver.get_screenshot_as_png()))
        im = im.crop((left, top, 950, bottom))  #crop screenshot so we only get the comment / template body
        screenshot_filename = 'artifacts/screenshots/screenshot_' + str(comment_i) + '_' + str(sentence_i)+ '.png'
        im.save(screenshot_filename)  #save screenshot as file

        #replaces bad and weird words in sentence with ad friendly child words
        speech = hf.cleanSpeech(sentence)

        #generates tts audio snippets and saves them in audios folder as mp3 files. Gets the file name
        audio_filename = ttsg.generate_tts(speech, comment_i, sentence_i)

        # iterate sentence counter
        sentence_i+=1

        #save screenshot and audio filenames to a list for sentences_list
        sentences_list.append([ screenshot_filename, audio_filename ])

    #iterate comment index
    comment_i+=1

    #add sentence_list to end of comments_list
    comments_list.append(sentences_list)


# open output file for writing json comments_list so moviepy_script can use the data
with open('artifacts/title/thread_comments.json', 'w') as filehandle:
    json.dump(comments_list, filehandle, indent=2)


driver.close() #close driver