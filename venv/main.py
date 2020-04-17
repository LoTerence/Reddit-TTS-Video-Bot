'''
reddit tts youtube bot for automating askreddit thread youtube video creation
This script saves screenshots and audios and saves the locations to a json
written by Terence Lo
'''
from string import Template
from selenium import webdriver
import json
import helpfulFuncs as hf
import ttsGenerator as ttsg


# First thing I have to do: Empty [audio, screenshots, clips] folders of old content
hf.empty_folder('artifacts/audio')
hf.empty_folder('artifacts/screenshots')


# Read comment_bodies jsons and save to vars
comment_body_list = []
with open('artifacts/jsons/comment_bodies.json', 'r') as filehandle:
    comment_body_list = json.load(filehandle)
filehandle.close()


# Prepare html templates
thread_template = hf.readTemplate("html_templates/threadTemplate.html")
comm_template = hf.readTemplate("html_templates/commentTemplate.html")


#TODO: might replace with a numpy list or something faster or numpy list of dicts
#make a list of comments that will contain lists representing the sentences of each comment
# [ comment0[ sentence0[ screenshot0, audio0 ], s1[ sc1, a1 ], s2[ sc2, a2 ] ... ]
#   c1[ s0[ sc0, a0 ], ...]
#   c2....
# ]
# the screenshot and audio are strings of the screenshot and audio's file name
# this will be saved to a json format so that it can be used by moviepy script later
ss_and_a = []   #as we loop through comments, we add its list of sents (screenshots and audio) to this list
comment_i = 0 #comment index


# instantiate selenium webdriver object (for screenshots later)
driver = webdriver.Chrome()
driver.fullscreen_window()


#loop through top n comments and get their child comments and split into sentences
for comment in comment_body_list:

    # ------We need the heights of body and text-area elements before iterating through sentences-------

    # list of text heights that should match with list of child comments for the comment thread
    text_height_list = []  #index 0 is parent comments height
    cid_i = 0

    # save content of comment['body'] to temporary str var
    body_sub = hf.convertLnToBr(comment['body'])  #change /n's to <br>
    sub = comm_template.substitute(bg_color=" ", margin_left=" ",
                                   username=comment['author'], karma=" ",
                                   awards=" ",
                                   text_height=" ", cId="cid0",
                                   commentbody=body_sub)

    threadDiv=Template(sub+"$newComment")

    # if the comment has a threadList, make a comment template with it.
    if comment["threadComments"]:
        for c in comment["threadComments"]:
            body_sub = hf.convertLnToBr(c['body'])  # save content of comment['body'] to temporary str var
            sub = comm_template.substitute(bg_color=" ", margin_left="margin-left:"+str(24*(cid_i+1))+"px;",
                                                username=c["author"], karma=" ",
                                                awards=" ",
                                                text_height=" ", cId="cid"+str(cid_i+1),
                                                commentbody=body_sub)
            threadDiv=Template(threadDiv.substitute(newComment=sub)+"$newComment")
            cid_i+=1

    sub=threadDiv.substitute(newComment=" ")

    hf.writeTemplate(thread_template.substitute(body_height=" ", commentsDiv=sub), 'html_templates/t_comments.html')
    driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/t_comments.html')  #open t_comments in driver
    body_height = 'height:'+ str(driver.find_element_by_id("bodyid").size["height"] +2)+'px;'  #get the height of thread body div
    text_height_list.append('height:'+ str(driver.find_element_by_id("cid0").size["height"] +2)+'px;') #get height of text area of parent comment
    if comment["threadComments"]:
        cid_i=1
        for c in comment["threadComments"]:
            text_height_list.append('height:'+ str(driver.find_element_by_id("cid"+str(cid_i)).size["height"] +2)+'px;') #get height of text area of child comment
            cid_i+=1

    # get the karma - convert comment['score'] to k's if over 999, else keep it the same
    karma = hf.convertNToK(comment['score'])

    #get the awardings list and check for gold to change bg_color
    awards = " "
    bg_color = " "
    if comment["all_awardings"]:
        awards=hf.awardListToTemplateStr(comment)
        if hf.checkForGold(comment):
            bg_color = "background-color: rgba(221, 189, 55, 0.1);"

    #split comment body into a list of sentences seperated by punctuation
    sentences = list(filter(None, hf.punctuation_regex.split(comment['body'])))
    print(sentences)  #test if I got the sentences right

    # make value for comment body substitute, as we loop through sentences we append sentences to commentBodySub
    commentBodySub = ''

    # sentence index per comment
    sentence_i = 0

    # sentences list: will contain lists representing the screenshot and audio. This will be added to ss_and_a at the end of the sentences loop
    sentences_list = []

    for sentence in sentences:

        #replace newlines in sentence with <br>
        sentence = hf.convertLnToBr(sentence)

        commentBodySub+=sentence #append sentence to comment body for the template

        # create html files with the template using individual sentences
        sub = comm_template.substitute(bg_color=bg_color, margin_left=" ",
                                       username=comment['author'], karma=karma,
                                       awards=awards,
                                       text_height=text_height_list[0], cId="cid0",
                                       commentbody=commentBodySub)
        tsub = thread_template.substitute(body_height=body_height, commentsDiv=sub)
        #open blank file for writing reddit comment html
        hf.writeTemplate(tsub, 'html_templates/t_comments.html')

        # take screenshot of reddit comment and save to screenshots folder
        driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/t_comments.html')

        if ((sentence=="<br>")or(sentence==" <br>")or(sentence==".")or(sentence=="\"")):
            print('Dont take screenshot or audio')
        else:
            screenshot_filename = 'artifacts/screenshots/screenshot_' + str(comment_i) + '_' + str(sentence_i) + '.png'
            hf.takeScreenshot(driver, screenshot_filename)

            #replaces bad and weird words in sentence with ad friendly child words
            speech = hf.cleanSpeech(sentence)

            #generates tts audio snippets and saves them in audios folder as mp3 files. Gets the file name
            audio_filename = 'artifacts/audio/voice_' + str(comment_i) + '_' + str(sentence_i) + '.mp3'
            ttsg.gen_tts(speech, audio_filename)

            #save screenshot and audio filenames to a list for sentences_list
            sentences_list.append([ screenshot_filename, audio_filename ])  # TODO: maybe change this to dict

            # iterate sentence counter
            sentence_i+=1
        #End if-else


    #Here we try to take screenshots of the sentences of all the threadComments
    if comment["threadComments"]:

        # Make an overall template var to append child comments to
        threadDiv = Template(sub + "$newComment")
        cid_i = 1

        for c in comment["threadComments"]:
            # get the karma - convert comment['score'] to k's if over 999, else keep it the same
            karma = hf.convertNToK(c['score'])

            # get the awardings list and check for gold to change bg_color
            awards = " "
            bg_color = " "
            if c["all_awardings"]:
                awards = hf.awardListToTemplateStr(c)
                if hf.checkForGold(c):
                    bg_color = "background-color: rgba(221, 189, 55, 0.1);"

            # split comment body into a list of sentences seperated by punctuation
            sentences = list(filter(None, hf.punctuation_regex.split(c['body'])))  #change this
            print(sentences)  # test if I got the sentences right

            # make value for comment body substitute, as we loop through sentences we append sentences to commentBodySub
            commentBodySub = ''

            for sentence in sentences:

                #replace newlines in sentence with <br>
                sentence = hf.convertLnToBr(sentence)

                commentBodySub+=sentence #append sentence to comment body for the template

                # create html files with the template using individual sentences
                csub = comm_template.substitute(bg_color=bg_color, margin_left="margin-left:"+str(24*cid_i)+"px;",
                                               username=c['author'], karma=karma,
                                               awards=awards,
                                               text_height=text_height_list[cid_i], cId="cid"+str(cid_i),
                                               commentbody=commentBodySub)
                sub = threadDiv.substitute(newComment=csub)
                tsub = thread_template.substitute(body_height=body_height, commentsDiv=sub)
                #open blank file for writing reddit comment html
                hf.writeTemplate(tsub, 'html_templates/t_comments.html')

                # take screenshot of reddit comment and save to screenshots folder
                driver.get('file://C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/html_templates/t_comments.html')

                if ((sentence == "<br>") or (sentence == ".")):
                    print('Dont take screenshot or audio')
                else:
                    screenshot_filename = 'artifacts/screenshots/screenshot_' + str(comment_i) + '_' + str(sentence_i) + '.png'
                    hf.takeScreenshot(driver, screenshot_filename)

                    #replaces bad and weird words in sentence with ad friendly child words
                    speech = hf.cleanSpeech(sentence)

                    #generates tts audio snippets and saves them in audios folder as mp3 files. Gets the file name
                    audio_filename = 'artifacts/audio/voice_' + str(comment_i) + '_' + str(sentence_i) + '.mp3'
                    ttsg.gen_tts(speech, audio_filename)

                    #save screenshot and audio filenames to a list for sentences_list
                    sentences_list.append([ screenshot_filename, audio_filename ])  # TODO: maybe change this to dict

                    # iterate sentence counter
                    sentence_i+=1
                #End if-else
            #End sentences for loop

            threadDiv = Template(sub + "$newComment")
            cid_i+=1
        #End c in commments for loop
    #End if threadComments

    #add sentence_list to end of ss_and_a
    ss_and_a.append(sentences_list)
    #iterate comment index
    comment_i+=1
#End for comment in comment_body_list for loop


# open output file for writing json ss_and_a so moviepy_script can use the data
with open('artifacts/jsons/screenshots_and_audios.json', 'w') as filehandle:
    json.dump(ss_and_a, filehandle, indent=2)


driver.close() #close driver