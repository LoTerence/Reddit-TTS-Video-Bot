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

# vars
top_n = 30   #number of comments to take screenshots of
#replace this url with new url every time you want to run the script on a new thread
thread_url = f"https://www.reddit.com/r/AskReddit/comments/foslu3/if_covid19_wasnt_dominating_the_news_right_now/"  #replace this url with new url every time you want to run the script on a new thread
comment_body_list = []

reddit_creds = {}
with open('misc/reddit.json', 'r') as filehandle:
    reddit_creds = json.load(filehandle)
filehandle.close()

# grab reddit comments with praw
r = praw.Reddit(client_id=reddit_creds["reddit_client_id"], client_secret=reddit_creds["reddit_client_secret"],
                     password=reddit_creds["reddit_pw"], user_agent=reddit_creds["reddit_user_agent"],
                     username=reddit_creds["reddit_user"])

##### -------  Replace this url with new url every time you want to run the script on a new askreddit post ------------------------------
thread = r.submission(url=thread_url)
thread.comment_sort = 'best' # get the best comments from the thread



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


#save comment_body_list json to txt
with open(f'artifacts/title/comment_body_json.txt', 'w') as filehandle:
    json.dump(comment_body_list, filehandle, indent=2)
    print('Saved comment_body_list to artifacts/title/comment_body_json.txt')