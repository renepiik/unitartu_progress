import tweepy
import datetime
from dotenv import dotenv_values
import date_scraper

# config
config = dotenv_values(".env")

auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
auth.set_access_token(config['ACCESS_KEY'], config['ACCESS_SECRET'])
api = tweepy.API(auth)


# ongoing semester start and end times
# UT does not provide any endpoint to get those dates easily so i have to resort to web crawling a page which might change at any time and fuck up this script, THANKS!
semester_start, semester_end = date_scraper.main()
today = datetime.date.today()

# progress x/100
semester_progress = round(((today - semester_start) * 100) / (semester_end - semester_start))

message = ""

if semester_progress > 100:
    message = "semester on läbi!"
elif semester_progress == 69:
    message = "nice"
elif semester_progress == 50:
    message = "klaas on pooltühi"

# convert it into y/15
mapped_progress = round((semester_progress / 100) * 15)

progress_bar = ''
for i in range(15):
    if i < mapped_progress:
        progress_bar = progress_bar + '▓'
    else:
        progress_bar = progress_bar + '░'

status = progress_bar + '  ' + str(semester_progress) + '%'

if len(message) != 0:
    status = status + '\n' + message

try:
    api.update_status(status)
    print('New Tweet posted!')
except Exception:
    print('Something went wrong. Have you already tweeted today?')
    logs = open('logs.txt', 'a')
    logs.write('Tweet with content "' + status + '" not posted at ' + str(datetime.datetime.now()) + '.\n')
    logs.close()
