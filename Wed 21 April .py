import pymysql.cursors
from datetime import datetime # make working with dates 1000x easier 
import time # become time lords
import random # create random numbers (probably not needed)
import requests # make http requests
import json # make sense of what the requests return

def database_setup():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
    user='computer',
    password='123',
    database='dev2qa',
    cursorclass= pymysql.cursors.DictCursor)
    return(connection)
    #with connection:

def add_user():
    username = input("what is your username?")
    password = input("Choose a password: ")
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
    connection.commit()

def retrieve_password(connection):
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `userid`, `password` FROM `users` WHERE `username`=%s"
        cursor.execute(sql, ('input search',))
        result = cursor.fetchone()
        print(result)

gameID = '252490'
cookie = {'steamLoginSecure': '123451234512345%ABC%ABC%123%123456ABC12345'};
icon_tag = 'https://community.akamai.steamstatic.com/economy/image/'
# itialize
allItemNames = [];
allIconUrls = [];
description = []
# find total number items
allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count=100', cookies=cookie); # get page
allItems = allItemsGet.content; # get page content

allItems = json.loads(allItems); # convert to JSON
totalItems = allItems['total_count']; # get total count
allItems = allItems['results'];

for item in allItems:
    description = item['asset_description']
    allItemNames.append(description['market_hash_name'])
    allIconUrls.append(description['icon_url'])
    print(item)


#connection = database_setup()
#retrieve_password(connection)