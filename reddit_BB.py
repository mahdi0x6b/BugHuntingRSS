import requests,urllib
import feedparser,json,time
from tinydb import TinyDB, Query
db = TinyDB(r'reddit.json')
article = Query()

discord_webhook = "https://discordapp.com/api/webhooks/*******/*********" #change
discord_channel_id = "5678745098327235" #change

urls =["https://reddit.com/r/netsec/new/.rss"]


#def notf(data):
#    #send telegram
#
#    ms = "[+] new post \n\n%s\n\npublishTime: %s\n\n<a href='%s'>article URL</a>"%(data.title,
#                                                                                      data.published,
#                                                                                      data.link)
#    token = ""
#    chat_id = ""
#    url_req = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=html"%(token,
#                                                                                         chat_id,
#                                                                                         urllib.parse.quote(ms))
#
#    results = requests.get(url_req)

def notf(data):
    title = data.title
    pubat = data.published
    link = data.link
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
          "title": "Link",
          "url": link,
          "description": "[+] new post\n\n%s\n"%(title),
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
    time.sleep(10)

def test(url):
    tree = feedparser.parse(url)

    for i, _ in enumerate(tree.entries):
        if not(db.search(article.title == tree.entries[i].title)):
            db.insert({'title': tree.entries[i].title, 'published': tree.entries[i].published,"link":tree.entries[i].link})
            print("[+] new article %s"%(tree.entries[i].title))
            notf(tree.entries[i])

if __name__ == "__main__":
    for i in urls:
        try:
            test(i)
        except:
            print("[x] Error: ",i)
