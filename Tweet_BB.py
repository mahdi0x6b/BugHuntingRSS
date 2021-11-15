import requests,urllib,uuid,datetime,json,twint,time
from tinydb import TinyDB, Query

db = TinyDB(r'tweet.json')
tweet = Query()

discord_webhook = "https://discordapp.com/api/webhooks/*******/*********" #change
discord_channel_id = "5678745098327235" #change

qus = ["#bugbountytips"] # search query list


#----------query example----------------------
#       "#bugbounty","#bugbountytips",
#       "#application-security",
#       "#penetration-testing","#writeup",
#       "#api-security","#bugbounties",
#       "#hacking","#pentest",
#       "#infosec","#cybersecurity"
#----------------------------------------

#---------telegram bot notf-----------
#def notf(data):
#    #send telegram
#    ms = "%s\n\nLike: %s\tRetweet: %s\tMention: %s\n\npublishTime: %s %s\n\n<a href='%s'>Tweet link</a>"%(data["tweet"],
#                                                                                                    data["likes_count"],
#                                                                                                    data["retweets_count"],
#                                                                                                    data["replies_count"],
#                                                                                                    data["date"],data["time"],
#                                                                                                    data["link"])
#    token = ""
#    chat_id = ""
#    url_req = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=html"%(token,
#                                                                                               chat_id,
#                                                                                               urllib.parse.quote(ms))
#
#    results = requests.get(url_req)
#--------------------------------------------------------


def notf(data):
    username = data["username"]
    name = data["name"]
    tweet = data["tweet"]
    like = data["likes_count"]
    Retweet = data["retweets_count"]
    Mention = data["replies_count"]
    pubat = "%s %s"%(data["date"],data["time"])
    tweet_url = data["link"]
    url = discord_webhook

    payload = json.dumps({
      "content": "",
      "channel_id": str(discord_channel_id),
      "allowed_mentions": {
        "parse": [
          "users"
        ]
      },
      "embeds": [
        {
          "color": 1942002,
          "author": {
            "name": "%s (@%s)"%(name,username),
            "url": "https://twitter.com/%s"%(username),
            "icon_url": "https://avatar-resolver.vercel.app/twitter/%s"%(username)
          },
          "title": "Tweet Link",
          "url": tweet_url,
          "description": "%s\n\nLike: %s\tRetweet: %s\tMention: %s\n"%(tweet,like,Retweet,Mention),
          "footer": {
            "text": "Posted at %s"%(pubat)
          }
        }
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(10) # discord webhook rate limit

def twintF(q,since,output):
    config = twint.Config()
    config.Search = q
    config.Since = str(since)
    config.Store_json = True
    config.Output = "%s.json"%(output)
    twint.run.Search(config)

def grab(query):
    fname = uuid.uuid4().hex +"_"+ str(datetime.date.today())
    since = datetime.date.today() - datetime.timedelta(days=2)
    twintF(query,since,fname)

    with open("%s.json"%(fname),"r") as r:
        lines = r.readlines()
        lines = [line.rstrip() for line in lines]

    for item in lines:
        item = json.loads(item)
        if not(db.search(tweet.id == item["id"])):
            q = {
                    "id":item["id"],
                    "conversation_id":item["conversation_id"],
                    "date":item["date"],
                    "time":item["time"],
                    "timezone":item["timezone"],
                    "user_id":item["user_id"],
                    "username":item["username"],
                    "name":item["name"],
                    "tweet":item["tweet"],
                    "language":item["language"],
                    "mentions":item["mentions"],
                    "urls":item["urls"],
                    "photos":item["photos"],
                    "replies_count":item["replies_count"],
                    "retweets_count":item["retweets_count"],
                    "likes_count":item["likes_count"],
                    "hashtags":item["hashtags"],
                    "cashtags":item["cashtags"],
                    "link":item["link"],
                    "retweet":item["retweet"],
                    "quote_url":item["quote_url"],
                    "video":item["video"],
                    "thumbnail":item["thumbnail"],
                    "source":item["source"],
                    "user_rt_id":item["user_rt_id"],
                    "user_rt":item["user_rt"],
                    "retweet_id":item["retweet_id"],
                    "reply_to":item["reply_to"],
                    "retweet_date":item["retweet_date"]
                }
            db.insert(q)
            notf(q)

    

def main():
    for i in qus:
        grab(i)

if __name__ == "__main__":
    main()
