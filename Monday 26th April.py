import pymysql.cursors #allows for input into sql database
import time # manage time
import random # allows for rng 
import requests # makes website requests
import json # reads website requests
from multiprocessing import Process #allows for multiple functions to run at once
import sys
import PySimpleGUI as sg

def SignupGui():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Sign Up')],
                [sg.Text('Username: '), sg.InputText()],
                [sg.Text('Password:  '), sg.InputText()],
                [sg.Button('Submit'), sg.Button('Cancel')] ]
    # Create the Window
    window1 = sg.Window('Sign Up', layout)
    openw1 = 1
    correct = 0
    # Event Loop to process "events" and get the "values" of the inputs
    while correct == 0:
        while openw1 == 1:
            event, values = window1.read()
            if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                break
            elif event =='Cancel':
                break
            elif event == 'Submit':
                print('You entered ', values[0])
                username = values[0]
                username = username.lower()
                print('You entered ', values[1])
                password = values[1]
                window1.close()
                openw1 = 0
        layout2 = [ [sg.Text('Confrim Your Details')],
                    [sg.Text("Your username is: " + values[0])],
                    [sg.Text("Your Password is: " + values[1])],
                    [sg.Button('Submit'), sg.Button('Cancel')] ]

        window2 = sg.Window('Confirmation', layout2)
        openw2 = 1
        while openw2 == 1:
            event2, values = window2.read()
            if event2 == sg.WIN_CLOSED or event2 == 'Cancel': # if user closes window or clicks cancel
                window2.close()
                break
            elif event2 == 'Submit':
                print("Successful Signup")
                window2.close()
                correct = 1
                openw2 == 0

    connection = database_setup()
    with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
    connection.commit()
    mainline()

def database_setup():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
    user='computer',
    password='123',
    database='dev2qa',
    cursorclass= pymysql.cursors.DictCursor)
    return(connection)
    #with connection:

def old_add_user():

    connection = database_setup()
    print("Signup Starting")
    confirmstart = input(("Press y to confirm: "))
    confirmstart = confirmstart.lower()
    while confirmstart == 'y':
        username = input("What is your username? ")
        username = username.lower()
        password = input("Choose a password: ")
        password = password.lower()
        print("Username:", username, "Password:", password)
        confirmdetails = input(("Press y to confirm: "))
        confirmstart = confirmstart.lower()
        if confirmdetails == 'y':
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
            connection.commit()
            confirmstart = input(("Add another user y/n"))
            confirmstart = confirmstart.lower()
            confirmdetails = 'n'

def retrieve_password(username):
    connection = database_setup()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `userid`, `password` FROM `users` WHERE `username`=%s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        return(result)

def table_setup():
    connection = database_setup()
    gameID = '252490' #rust game id
    cookie = {'steamLoginSecure': '123451234512345%ABC%ABC%123%123456ABC12345'}
    allItemNames = []
    allIconUrls = []
    allItemPrices = []  # establish arrays
    allItemListings = []
    completedskins = []
    useragents = ['Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobile Safari (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3613.1 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; SM-T510 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.116 Safari/537.36'
    ] 
    #uses these servers to ping steam to help limit timeouts
    allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count=100', cookies=cookie);
    # gets list of all skins
    allItems = allItemsGet.content # returns contents of request
    allItems = json.loads(allItems) # convert to JSON array
    totalItems = allItems['total_count'] #checks the total number of items
    #can only loop through in batches of 100 max
    #goes through and gives updates every 50 instead
    for currPos in range(0,totalItems+50,50): # go through all the items
        time.sleep(random.uniform(12, 20)) # steam thinks ur a robot if u ping in even intervals 
        serverid = random.randint(0,9)
        server = useragents[serverid] #selects a random user agent for every ping requests
        allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?start='+str(currPos)+'&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count=5000', headers = ({'User-agent': server}), cookies=cookie)
        #finds skins based on current position, uses cookie(user code) and useragent when pinging
        print('Items '+str(currPos)+' out of '+str(totalItems)+' code: '+str(allItemsGet.status_code)) 
        #status code 200 means all is good, prints current position in cycle, (code 429 means u have overpinged)
        allItems = allItemsGet.content
        allItems = json.loads(allItems)
        allItems = allItems['results'] #loads "results" content of json file

        for item in allItems:
            description = item['asset_description']
            Name = description['market_hash_name']
            Name = Name.replace(" ", "_")
            Name = Name.replace("'", "")       #removes all apostrophies and speechmarks, replaces spaces with underscores
            Name = Name.replace('"', "")       #allows for names to be stored in database
            Price = Price = item['sell_price']
            Icon_Url = description['icon_url'] #gets current price, volume sold and picture
            Listings = item['sell_listings']
            if Name in completedskins:
                a = 0
            else:
                    with connection.cursor() as cursor:
                        # Create a new record in database
                        sql = "INSERT INTO `rustskins` (`skinname`, `iconurl`, `price`, `listings`) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (Name, Icon_Url, Price, Listings)) 
                        completedskins.append(Name) #adds name to list to avoid repititon (name is primary key)
            connection.commit() #commits the file to mysql

def updater():
        connection = database_setup()
        gameID = '252490'
        cookie = {'steamLoginSecure': '123451234512345%ABC%ABC%123%123456ABC12345'}
        allItemNames = []
        allIconUrls = []
        allItemPrices = []
        allItemListings = []
        completedskins = []
        useragents = ['Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobile Safari (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3613.1 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; SM-T510 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.116 Safari/537.36'
        ]
    
        allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count=100', cookies=cookie); # get page
        allItems = allItemsGet.content 
        allItems = json.loads(allItems) 
        totalItems = allItems['total_count']
        for currPos in range(0,totalItems+50,50): 
            time.sleep(random.uniform(12, 20)) 
            b = useragents[a]
            
            allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?start='+str(currPos)+'&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count=5000', headers = ({'User-agent': b}), cookies=cookie)
            print('Items '+str(currPos)+' out of '+str(totalItems)+' code: '+str(allItemsGet.status_code)) # reassure us the code is running and we are getting good returns (code 200)
            
            allItems = allItemsGet.content
            allItems = json.loads(allItems)
            allItems = allItems['results']

            for item in allItems:
                description = item['asset_description']
                Name = description['market_hash_name']
                Name = Name.replace(" ", "_")
                Name = Name.replace("'", "")
                Name = Name.replace('"', "")    
                Price = Price = item['sell_price']
                Icon_Url = description['icon_url']
                Listings = item['sell_listings']
                if Name in completedskins:
                    a = 0
                else:
                        with connection.cursor() as cursor:
                            #o
                            sql = "update rustskins set price ='{price}' where skinname='{name}'".format(price=Price, name= Name)      
                            sql1= "update rustskins set listings ='{price}' where skinname='{name}'".format(price=Listings, name= Name)    
                            #contributes live price and volume to database
                            cursor.execute(sql)
                            cursor.execute(sql1)        
                            completedskins.append(Name)     #avoid repitions
                connection.commit()

def slowprint(s):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

def login():
    slowprint("Welcome to login")
    slowprint("Enter Username: ")
    Username = input()
    Username = Username.lower()
    slowprint("Enter Password: ")
    password = input()
    userdetails = retrieve_password(Username)
    userpass = userdetails['password']
    UserId = userdetails['userid']
    if password == userpass:
        slowprint("Login Successfull")
        return(UserId)
    else:
        slowprint("Invalid Username or Password")

def mainline(choose):
    while choose == 't':
        slowprint("Welcome to the Rust Manager")
        slowprint("1. Signup (GUI)")
        slowprint("2. Login")
        slowprint("3. Price Updater")
        slowprint("Choose your destination: ")
        MenuSelection = input()
        if MenuSelection == '1':
            SignupGui()
        elif MenuSelection == '2':
            UserID = login()
            choose = 'n'
        elif MenuSelection == '3':
            updater()
        else:
            slowprint("Invalid Input")
    print(UserID)

choose = 't'
mainline(choose)
#mainline(choose)
# the join means wait untill it finished

#retrieve_password(connection)
icon_tag = 'https://community.akamai.steamstatic.com/economy/image/' #put icon url after this to retrieve i