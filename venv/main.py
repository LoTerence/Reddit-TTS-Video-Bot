'''
reddit tts youtube bot for automating askreddit thread youtube video creation
written by Terence Lo
'''
from string import Template
from selenium import webdriver
import json
import helpfulFuncs as hf
import ttsGenerator as ttsg


# First thing I have to do: Empty [audio, screenshots, clips] folders of old content
hf.empty_folder('artifacts/audio')
hf.empty_folder('artifacts/clips')
hf.empty_folder('artifacts/screenshots')


# Read comment_body_list json and save to variable comments_list
title_dict = {}
with open('artifacts/title/submission.json', 'r') as filehandle:
    title_dict = json.load(filehandle)
filehandle.close()
comment_body_list = []
with open('artifacts/title/comment_bodies.json', 'r') as filehandle:
    comment_body_list = json.load(filehandle)
filehandle.close()


# Prepare html templates
f = open("html_templates/submissionTemplate.html","r")   #for title/submission screenshot
title_template = Template(f.read())
f.close()
f = open("html_templates/awardTemplate.html","r")  #award template
award_template = Template(f.read())
f.close()
f = open("html_templates/threadTemplate.html","r")  #thread template
thread_template = Template(f.read())
f.close()
f = open("html_templates/commentTemplate.html")  #single comment template
comm_template = Template(f.read())
f.close()

#TODO: might replace with a numpy list or something faster or numpy list of dicts
#make a list of comments that will contain lists representing the sentences of each comment
# [ comment0[ sentence0[ screenshot0, audio0 ], s1[ sc1, a1 ], s2[ sc2, a2 ] ... ]
#   c1[ s0[ sc0, a0 ], ...]
#   c2....
# ]
# the screenshot and audio are strings of the screenshot and audio's file name
# this will be saved to a json format so that it can be used by moviepy script later
comments_list = []   #as we loop through comments, we add its list of sents (screenshots + audio) to this list
#make a value for the comment iterator:
comment_i = 0 #comment index


# instantiate selenium webdriver object (for screenshots later)
driver = webdriver.Chrome()
driver.fullscreen_window()


awards= " "
if title_dict["all_awardings"]:
    awards = ""
    for award in title_dict["all_awardings"]:
        s = award_template.substitute(img_url=award["icon"], awardCount=str(award["count"]))
        awards+=s


# Take a screenshot of the title/OP/thread title+text
sub = title_template.substitute(score=hf.convertNToK(title_dict["score"]),
                                username= 'u/' + title_dict["username"],
                                awards=awards,
                                thread_title=title_dict["title"],
                                text=title_dict["selftext"],
                                num_comments=hf.convertNToK(title_dict["num_comments"]))
f = open('html_templates/submissionPost.html', 'w') # open blank file for writing reddit submission html
f.write(sub)  # write the html template with the comment data substituted in
f.close()
driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/submissionPost.html')
#save screenshot and tts of title in title folder
hf.takeScreenshot(driver, 'artifacts/title/CAPTURE.png')
ttsg.gen_tts(title_dict["title"], 'artifacts/title/title_tts.mp3')


#loop through top n comments and get their child comments and split into sentences
for comment in comment_body_list:

    #get the height of the comment text area
    comment_temp = comment['body']  # save content of comment['body'] to temporary str var
    comment_temp = hf.convertLnToBr(comment_temp)
    sub = comm_template.substitute(username=comment['author'], karma=" ", bg_color=" ",
                                      awards=" ", text_height=" ", commentbody=comment_temp, margin_left=" ",
                                   childComment="")
    sub = thread_template.substitute(commentsDiv=sub)
    f = open('html_templates/t_comments.html', 'w') # open blank file for writing reddit comment html
    f.write(sub)  # write the html template with the comment data substituted in
    f.close()
    driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/t_comments.html')
    comment_height = 'height:'+ str(driver.find_element_by_id("comment").size["height"] +2)+'px'  #get the height of comment text area

    # get the karma - convert comment['score'] to k's if over 999, else keep it the same
    karma = hf.convertNToK(comment['score'])

    # get the awardings list
    awards = " "
    bg_color = " "
    if comment["all_awardings"]:
        awards = ""
        for award in comment["all_awardings"]:
            s = award_template.substitute(img_url=award["icon"], awardCount=str(award["count"]))
            awards += s
            if (award["name"] == "Gold") or (award["name"] == "Platinum"):
                bg_color = "background-color: rgba(221, 189, 55, 0.1)"

    # Split the comment into sentences
    #split comment body into a list of sentences seperated by punctuation
    comment_temp = comment['body']
    sentences = list(filter(None, hf.punctuation_regex.split(comment_temp)))
    print(sentences)  #test if I got the sentences right

    commentBodySub = ''  # make value for comment body substitute, as we loop through sentences we append sentences to commentBodySub

    sentence_i = 0 #sentence index per comment

    # sentence list: will contain lists representing the screenshot and audio
    # this will then be added to comment_list at the end of the sentences loop
    sentences_list = []  # TODO: maybe change this to dict

    for sentence in sentences:

        #replace newlines in sentence with <br>
        sentence = hf.convertLnToBr(sentence)

        commentBodySub+=sentence #append sentence to comment body for the template

        # create html files with the template using individual sentences
        sub = comm_template.substitute(username=comment['author'], karma=karma, bg_color=bg_color,
                                          awards=awards, text_height=comment_height,
                                       commentbody=commentBodySub, margin_left=" ",
                                       childComment="")
        tsub = thread_template.substitute(commentsDiv=sub)
        #open blank file for writing reddit comment html
        f = open('html_templates/t_comments.html', 'w')
        f.write(tsub) #write the html template with the comment data substituted in
        f.close() #save the write

        # take screenshot of reddit comment and save to screenshots folder
        driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/t_comments.html')
        screenshot_filename = 'artifacts/screenshots/screenshot_' + str(comment_i) + '_' + str(sentence_i) + '.png'
        hf.takeScreenshot(driver, screenshot_filename)

        #replaces bad and weird words in sentence with ad friendly child words
        speech = hf.cleanSpeech(sentence)

        #generates tts audio snippets and saves them in audios folder as mp3 files. Gets the file name
        audio_filename = 'artifacts/audio/voice_' + str(comment_i) + '_' + str(sentence_i) + '.mp3'
        ttsg.gen_tts(speech, audio_filename)

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