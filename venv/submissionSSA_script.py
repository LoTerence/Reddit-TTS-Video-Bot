'''
the script for getting the submission's screenshots and audio files
written by Terence Lo
'''
from string import Template
from selenium import webdriver
import json
import helpfulFuncs as hf
import ttsGenerator as ttsg


#Empty old folders
hf.empty_folder('artifacts/submission/audio')
hf.empty_folder('artifacts/submission/screenshots')


# Read title_dict and comment_bodies jsons and save to vars
title_dict = {}
with open('artifacts/submission/submission.json', 'r') as filehandle:
    title_dict = json.load(filehandle)
filehandle.close()


# Prepare html templates
title_template = hf.readTemplate("html_templates/submissionTemplate.html")


# instantiate selenium webdriver object (for screenshots later)
driver = webdriver.Chrome()
driver.fullscreen_window()


#vars
# list for saving locations of submission screenshots and audios
self_ss_and_a = []

#getting awards
awards = " "  # get submission awards list html
if title_dict["all_awardings"]:
    awards=hf.awardListToTemplateStr(title_dict)
selftext_sub = hf.convertLnToBr(title_dict["selftext"])

#get karma
karma = hf.convertNToK(title_dict["score"])

#get number of comments
num_comments = hf.convertNToK(title_dict["num_comments"])

#first get the height of self text area
sub = title_template.substitute(score=karma,
                                username= 'u/' + title_dict["username"],
                                awards=awards,
                                thread_title=title_dict["title"],
                                height=" ",
                                text=selftext_sub,
                                num_comments=num_comments)
hf.writeTemplate(sub,'html_templates/submissionPost.html')
driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/submissionPost.html')
text_height = 'height:'+ str(driver.find_element_by_id("comment").size["height"] +2)+'px;'


#initial screenshot with just the submission title
sub = title_template.substitute(score=karma,
                                username= 'u/' + title_dict["username"],
                                awards=awards,
                                thread_title=title_dict["title"],
                                height=text_height,
                                text=" ",
                                num_comments=num_comments)
hf.writeTemplate(sub,'html_templates/submissionPost.html')
driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/submissionPost.html')
hf.takeScreenshot(driver, 'artifacts/submission/screenshots/selftext0.png')  #save screenshot and tts of title in submission folder
ttsg.gen_tts(title_dict["title"], 'artifacts/submission/audio/selftext0.mp3')
self_ss_and_a.append(['artifacts/submission/screenshots/selftext0.png','artifacts/submission/audio/selftext0.mp3'])


#split self text into sentences and loop through sentences to save screenshots and audios
sentences = list(filter(None, hf.punctuation_regex.split(title_dict["selftext"])))
print(sentences)  #test if I got the sentences right
selftext_sub = ''
title_i = 1  # for keeping count of submission screenshots and audios
for sentence in sentences:
    sentence = hf.convertLnToBr(sentence)
    selftext_sub+=sentence
    sub = title_template.substitute(score=karma,
                                    username='u/' + title_dict["username"],
                                    awards=awards,
                                    thread_title=title_dict["title"],
                                    height=text_height,
                                    text=selftext_sub,
                                    num_comments=num_comments)
    hf.writeTemplate(sub, 'html_templates/submissionPost.html')
    #driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/submissionPost.html')
    if ((sentence == "<br>") or (sentence == " <br>") or (sentence == ".") or (sentence == "\"")):
        print('Dont take screenshot or audio')
    else:
        driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/submissionPost.html')
        hf.takeScreenshot(driver, 'artifacts/submission/screenshots/selftext'+str(title_i)+'.png')  # save screenshot and tts of self text in submission folder
        speech = hf.cleanSpeech(sentence)
        ttsg.gen_tts(speech, 'artifacts/submission/audio/selftext'+str(title_i)+'.mp3')
        self_ss_and_a.append(['artifacts/submission/screenshots/selftext'+str(title_i)+'.png', 'artifacts/submission/audio/selftext'+str(title_i)+'.mp3'])
        title_i+=1
    #END if else
#END for sentence in sentences - self text screenshots and audio


# open output file for writing json title_ss_and_a so moviepy_script can use the data
with open('artifacts/jsons/submission_ssa.json', 'w') as filehandle:
    json.dump(self_ss_and_a, filehandle, indent=2)


#close driver
driver.close()

#END submisisonSSA_script.py