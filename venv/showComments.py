'''
showComments.py
written by Terence Lo

take title and original submission data and save them to json
take best n comments from askreddit thread and save them to another json
be able to modify jsons
upload jsons to main.py
'''
import praw, json
import helpfulFuncs as hf
import pprint
from random import shuffle


# ---------   replace this url with new url every time you want to run the script on a new thread    ----------------------
thread_url = "https://www.reddit.com/r/AskReddit/comments/fynxsa/what_is_a_sign_that_youre_unattractive/?sort=top"
top_n = 20   #number of comments to take screenshots of
comment_body_list = []


# get credentials for reddit
reddit_creds = {}
with open('misc/reddit.json', 'r') as filehandle:
    reddit_creds = json.load(filehandle)
filehandle.close()


# grab reddit comments with praw
r = praw.Reddit(client_id=reddit_creds["reddit_client_id"], client_secret=reddit_creds["reddit_client_secret"],
                     password=reddit_creds["reddit_pw"], user_agent=reddit_creds["reddit_user_agent"],
                     username=reddit_creds["reddit_user"])
thread = r.submission(url=thread_url)
thread.comment_sort = 'top' # get the top comments from the thread, shuffle the comments later
#print(thread.title)
#pprint.pprint(vars(thread))  #see all of the thread variables

#make a list of awards
all_awardings = hf.get_awardings(thread.all_awardings)

# grab data from the askreddit thread title
title_dict = {
    "username": str(thread.author),
    "title": thread.title,
    "selftext": thread.selftext,
    "score": thread.score,
    "num_comments": thread.num_comments,
    "nsfw": thread.over_18,
    "all_awardings": all_awardings,
}

#save title_dict to json
with open(f'artifacts/jsons/submission.json', 'w') as filehandle:
    json.dump(title_dict, filehandle, indent=2)
    print('Saved title_dict to artifacts/jsons/submission.json')
filehandle.close()


#loop through top_n comments and save the text to json list
for comment in thread.comments[:top_n]:
    d = hf.createCommentDict(comment)
    d["threadComments"] = []
    c = comment.replies
    c.replace_more(limit=0)  #removes moreComments instances in comment.replies
    c = c.list()  #get the list of child comments
    if c:
        print(c[0])
        d["threadComments"].append(hf.createCommentDict(c[0]))
        next = c[0]
        nextC = next.replies
        nextC.replace_more(limit=0)
        nextC = nextC.list()
        if nextC:
            print(nextC[0])
            d["threadComments"].append(hf.createCommentDict(nextC[0]))

    print('Added comment by author: ' + d["author"])
    comment_body_list.append(d)

#shuffle the order of top comments
shuffle(comment_body_list)
#save comment_body_list json
with open(f'artifacts/jsons/comment_bodies.json', 'w') as filehandle:
    json.dump(comment_body_list, filehandle, indent=2)
    print('Saved comment_body_list to artifacts/submission/comment_bodies.json')
filehandle.close()
