import tweepy
import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")

auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
auth.set_access_token(config['ACCESS_KEY'], config['ACCESS_SECRET'])
api = tweepy.API(auth)

semester_start = datetime.date(day=6, month=2, year=2021)
today = datetime.date.today()
semester_end = datetime.date(day=26, month=6, year=2021)

# progress x/100
semester_progress = round(((today - semester_start) * 100) / (semester_end - semester_start))

# convert it into y/15
mapped_progress = round((semester_progress / 100) * 15)

progress_bar = ''
for i in range(15):
    if i < mapped_progress:
        progress_bar = progress_bar + '▓'
    else:
        progress_bar = progress_bar + '░'

status = progress_bar + '  ' + str(semester_progress) + '%'

try:
    api.update_status(status)
    print('New Tweet posted!')
except Exception:
    print('Something went wrong. Have you already tweeted today?')
    logs = open('logs.txt', 'a')
    logs.write('Tweet with content "' + status + '" not posted at ' + str(datetime.datetime.now()) + '.\n')
    logs.close()
