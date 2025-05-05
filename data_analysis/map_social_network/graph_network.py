#!pip install pandas pymongo
import pandas as pd
import pymongo
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient('mongodb://localhost:27017/pinterest-clone') # from .env
db = client['pinterest-clone']

# make a df for each collection
boards = pd.DataFrame(list(db.boards.find()))
comments = pd.DataFrame(list(db.comments.find()))
pins = pd.DataFrame(list(db.pins.find()))
users = pd.DataFrame(list(db.users.find()))

# create csv for links
relationships = []
for _, user in users.iterrows():
    for follower in user['followers']:
        relationships.append({
            'username': user['username'],
            'user_id': user['_id'],
            'follower': db.users.find_one({'_id': follower})['username'],
            'follower_id': follower
        })
links = pd.DataFrame(relationships)
links.to_csv('users_links.csv', index=False)

# create csv for nodes
user_info = []
for _, user in users.iterrows():
    user_info.append({
        'username': user['username'],
        'location': user['location'],
        'country': user['location'].split(",")[-1],
        'follower_count': len(user['followers']),
        'following_count': len(user['following']),
        #'interests':user['interests'], # all blank
        'session_duration': user['sessionDuration'],
        'activity_score': user['activityScore'],
        #'segment': user['segment'],  # all are casual
        'login_count':user['loginCount']
    })
nodes = pd.DataFrame(user_info)
nodes.to_csv('users_nodes.csv', index=False)