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


# ---------   replace this url with new url every time you want to run the script on a new thread    ----------------------
thread_url = "https://www.reddit.com/r/AskReddit/comments/fu5ac0/exhomeless_redditors_what_was_the_scariest_thing/"
top_n = 30   #number of comments to take screenshots of
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
thread.comment_sort = 'best' # get the best comments from the thread
#print(thread.title)
#pprint.pprint(vars(thread))  #see all of the thread variables
'''x = thread.comments[0].replies
print(' ')
print('replies: ')
print(x)
print(' ')
print('replies vars: ')
pprint.pprint(vars(x))  #see all of the thread variables
xl = x.list()
print(' ')
print('list: ')
print (xl)
x.replace_more(limit=0)  #remove moreComment instances
print(' ')
print('list 2: ')
print (x.list())
print(' ')'''
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
#print(title_dict)

#save title_dict to json
with open(f'artifacts/title/submission.json', 'w') as filehandle:
    json.dump(title_dict, filehandle, indent=2)
    print('Saved title_dict to artifacts/title/submission.json')
filehandle.close()


#loop through top_n comments and save the text to json list
for comment in thread.comments[:top_n]:
    d = hf.createCommentDict(comment)
    print('Added comment by author: ' + d["author"])
    c = comment.replies
    c.replace_more(limit=0)  #removes moreComments instances in comment.replies
    cd = c.list()  #get the list of child comments
    print('c list: ')
    print(cd)
    if cd:
        print(cd[0])
        d["topReply"] = hf.createCommentDict(cd[0])
    else:
        print('cd doesnt exist')
        d["topReply"] = {}
    comment_body_list.append(d)


#save comment_body_list json
with open(f'artifacts/title/comment_bodies.json', 'w') as filehandle:
    json.dump(comment_body_list, filehandle, indent=2)
    print('Saved comment_body_list to artifacts/title/comment_bodies.json')
filehandle.close()
