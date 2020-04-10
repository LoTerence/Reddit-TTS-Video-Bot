'''
showComments.py
written by Terence Lo

take best n comments from askreddit thread
save them to json
be able to modify json
upload json to main.py
'''
import praw, json
import helpfulFuncs as hf
#import pprint

# vars
top_n = 30   #number of comments to take screenshots of
# ---------   replace this url with new url every time you want to run the script on a new thread    ----------------------
thread_url = f"https://www.reddit.com/r/AskReddit/comments/foslu3/if_covid19_wasnt_dominating_the_news_right_now/"
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

#make a list of awards
#append platinum, gold and silver awards first:
all_awardings = []
for award in thread.all_awardings:
    if award["name"] == "Platinum":
        #award_dict = hf.createAward(award)
        all_awardings.append(hf.createAward(award))
        print('Appended '+award["name"])
        break
for award in thread.all_awardings:
    if award["name"] == "Gold":
        #award_dict = hf.createAward(award)
        all_awardings.append(hf.createAward(award))
        print('Appended '+award["name"])
        break
for award in thread.all_awardings:
    if award["name"] == "Silver":
        #award_dict = hf.createAward(award)
        all_awardings.append(hf.createAward(award))
        print('Appended '+award["name"])
        break
for award in thread.all_awardings:
    if ((award["name"] == "Platinum") or (award["name"] == "Gold") or (award["name"] == "Silver")):
        print('already added')
    else:
        all_awardings.append(hf.createAward(award))
        print('Appended '+award["name"])

# grab data from the askreddit thread title
title_dict = {
    "username": str(thread.author),
    "title": thread.title,
    "selftext": thread.selftext,
    "score": thread.score,
    "num_comments": thread.num_comments,
    "nsfw": thread.over_18,
    "upvote_ratio": thread.upvote_ratio,
    "all_awardings": all_awardings,
    #"all_awardings": thread.all_awardings,
}
#print(title_dict)

#save title_dict to json
with open(f'artifacts/title/submission.json', 'w') as filehandle:
    json.dump(title_dict, filehandle, indent=2)
    print('Saved title_dict to artifacts/title/submission.json')
filehandle.close()

'''
#loop through top_n comments and save the text to json list
for comment in thread.comments[:top_n]:
    d = {
        "body": " ",
        "author": " ",
        "score": 0
    }  # TODO: add gilding data
    comment_temp = hf.deEmojify(comment.body)  # de-emojify to quickfix charset bug  TODO:refine charset bug fix
    comment_temp = hf.deLinkify(comment_temp)  # remove http links
    d["body"] = comment_temp
    d["author"] = str(comment.author)
    d["score"] = comment.score
    print('Added comment by author: ' + d["author"])
    comment_body_list.append(d)


#save comment_body_list json
with open(f'artifacts/title/comment_bodies.json', 'w') as filehandle:
    json.dump(comment_body_list, filehandle, indent=2)
    print('Saved comment_body_list to artifacts/title/comment_bodies.json')
filehandle.close()
'''