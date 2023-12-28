import os
import tweepy
import time
import random
from tinydb import TinyDB, Query

API_KEY = #Enter API Key here
API_SECRET = #Enter API Secret Key here
ACCESS_TOKEN = #Enter Access Token here
ACCESS_SECRET = #Enter Access Secret here
bearer_tokens = #Enter bearer tokens here

client = tweepy.Client(consumer_key=API_KEY,
                       consumer_secret=API_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_SECRET)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


input_file = #The name of the video file

    
with open('frame_info.txt', 'r+') as file:
    frame_info = file.readline().split()
    frame_number = int(frame_info[0])
    max_frames = int(frame_info[1])


if frame_number < 1 or frame_number > max_frames:
    print("Invalid frame number!")
    exit()


directory = os.path.dirname(input_file)


previous_temp_file = os.path.join(directory, 'temp.jpg')
if os.path.exists(previous_temp_file):
    os.remove(previous_temp_file)


output_file = os.path.join(directory, 'temp.jpg')
ffmpeg_command = 'ffmpeg -i {} -vf "select=gte(n\,{})" -vframes 1 {}'.format(input_file, frame_number - 1, output_file)


os.system(ffmpeg_command)

print("Frame extracted and saved as", output_file)


media = api.media_upload("temp.jpg")

client.create_tweet(media_ids=[media.media_id])


db = TinyDB('random_numbers_db.json')

random_numbers = db.all()

while True:
    frame_number = random.randint(212, max_frames)
    if frame_number not in random_numbers:
        break
db.insert({'random_number': frame_number})
db.close()



with open('frame_info.txt', 'w') as file:
    file.write('{} {}'.format(frame_number, max_frames))
