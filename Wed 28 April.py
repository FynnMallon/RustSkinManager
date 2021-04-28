import pymysql.cursors #allows for input into sql database
import time # manage time
import random # allows for rng 
import requests # makes website requests
import json # reads website requests
from multiprocessing import Process #allows for multiple functions to run at once
import sys
import PySimpleGUI as sg

def SignupGui(): #Fully Functioning
    connection = database_setup() #establishes connection variable for pymysql
    correct = 0 #creates a loop
    while correct == 0:
        sg.ChangeLookAndFeel('LightGrey1')   # Design Colour
        # Design of login screen
        SignUp = [  [sg.Text('Sign Up')],
                    [sg.Text('Username: '), sg.InputText()],
                    [sg.Text('Password:  '), sg.InputText()],
                    [sg.Button('Submit'), sg.Button('Cancel')] ]
        
        window1 = sg.Window('Sign Up', SignUp, resizable=True, element_justification='c', location = (0, 0))  #creates popup window called signup
        openw1 = 1      
        event = ''
        values = '' #establishes varliables as null for loop
        event2 = ''

        while openw1 == 1: #creates loop for window 1 to read signup window
            event, values = window1.read() #reads the signup window for button presses and text entries
            if event == sg.WIN_CLOSED: # checks if window is closed
                correct = 1
                break
            elif event =='Cancel': #checks if button 'cancel' is pressed
                correct = 1
                break
            elif event == 'Submit':     # checks if submit is pressed
                print('You entered ', values[0])
                username = values[0]
                username = username.lower()         #takes values from window and assigns them to username and password
                print('You entered ', values[1])
                password = values[1]
                window1.close()
                openw1 = 0

        Confirm = [ [sg.Text('Confrim Your Details')],      #establishes layout for confirmation page
                    [sg.Text("Your username is: " + values[0])],
                    [sg.Text("Your Password is: " + values[1])],
                    [sg.Button('Submit'), sg.Button('Cancel')] ]

        Invalid = [ [sg.Text('Username Not Available')],    #establishes layout for invalid username (taken)
                    [sg.Text('Please try again')],
                    [sg.Button('Confirm')]  ]
        
        Successful = [ [sg.Text('Successful Signup')],    #establishes layout for invalid username (taken)
                    [sg.Text('Please Log In')],
                    [sg.Button('Confirm')]  ]

        window2 = sg.Window('Confirmation', Confirm, resizable=True, element_justification='c', location = (0, 0)) #creates confirmation window
        openw2 = 1
        while openw2 == 1: #creates loop for reading of cornfirmation window
            event2, values = window2.read()     #reads button presses for confirmation window
            if event2 == sg.WIN_CLOSED or event2 == 'Cancel': # if user closes window or clicks cancel
                window2.close()
                break
            elif event2 == 'Submit': #if submit is clicked 
                window2.close()
                time.sleep(1)
        with connection.cursor() as cursor:
        # Read a single record
            sql = "SELECT `userid` FROM `users` WHERE `username`=%s"
            cursor.execute(sql, (username,))    #checks username against records in users database
            result = cursor.fetchone()  
            if result is None:      #if result is None(NullType/Empty)
                window3 = sg.Window('Success', Successful, resizable=True, element_justification='c', location = (0, 0))#create successful window
                close = 'n'
                while close == 'n':
                    event3, values = window3.read() #reads window
                    if event3 == 'Confirm':
                        close = 'y' #checks if confirm is pressed
                        window3.close()
                    elif event3 == sg.WINDOW_CLOSED: #checks if window closed
                        close = 'y'
                        window3.close() 
                correct = 1 #breaks loop
                openw2 == 0
            else:   
                window3 = sg.Window('Invalid Username', Invalid, resizable=True, element_justification='c', location = (0, 0)) #creates invalid window
                close = 'n'
                while close == 'n':
                    event3, values = window3.read()
                    if event3 == 'Confirm': #checks if confirm pressed
                        close = 'y' 
                        window3.close()
                        correct = 0
                    elif event3 == sg.WINDOW_CLOSED:    #checks if window closed
                        close = 'y'
                        window3.close()
                        correct = 0 

    with connection.cursor() as cursor:
                # Create a new record if all above criteria is met
                sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))
    connection.commit() #commits to database

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
    sg.ChangeLookAndFeel('LightGrey1')
    loop = 1
    username = ''
    password = ''
    events = ''
    values = ''
    Login = [   [sg.Text("Please Input Username and Password")],
                [sg.Text("Username: "), sg.InputText()],
                [sg.Text("Password: "), sg.InputText()],
                [sg.Button("Submit"), sg.Button("Cancel")]
                ]
    Invalid = [ [sg.Text('Username or Password not correct')],    #establishes layout for invalid username (taken)
                    [sg.Text('Please try again')],
                    [sg.Button('Confirm')]  ]
        
    Successful = [ [sg.Text('Successful Login')],    #establishes layout for invalid username (taken)
                    [sg.Text('Please Continue to Main Menu')],
                    [sg.Button('Confirm')]  ]

    LoginWindow = sg.Window("Login", Login, resizable=True, element_justification='c', location = (0, 0), )
    while loop == 1:
        events, values = LoginWindow.read()
        if events == "Submit":
            username = values[0]
            password = values[1]
            loop = 0
            LoginWindow.close()
            userdetails = retrieve_password(username)
            userpass = userdetails['password']
            UserId = userdetails['userid']
            if password == userpass:
                window3 = sg.Window('Success', Successful, resizable=True, element_justification='c', location = (0, 0))#create successful window
                close = 'n'
                while close == 'n':
                    event3, values = window3.read() #reads window
                    if event3 == 'Confirm':
                        close = 'y' #checks if confirm is pressed
                        window3.close()
                        return(UserId)
                    elif event3 == sg.WINDOW_CLOSED: #checks if window closed
                        close = 'y'
                        window3.close() 
            else:   
                window3 = sg.Window('Invalid', Invalid, resizable=True, element_justification='c', location = (0, 0)) #creates invalid window
                close = 'n'
                while close == 'n':
                    event3, values = window3.read()
                    if event3 == 'Confirm': #checks if confirm pressed
                        close = 'y' 
                        window3.close()
                    elif event3 == sg.WINDOW_CLOSED:    #checks if window closed
                        close = 'y'
                        window3.close()
        elif events == sg.WINDOW_CLOSED:
            LoginWindow.close()
            loop = 0
        elif events == "Cancel":
            LoginWindow.close()
            loop = 0


def mainline(choose):
    UserID = 'None'
    while choose == 't':
        events = ''
        Values = ''
        Menu = ''
        cont = 0
        bigloop = ''
        favloop = ''
        favevents = ''
        favValues = ''
        UserID = 3 #testing purposes
        sg.ChangeLookAndFeel('LightGrey1')

        Menu = [    [sg.Text("Welcome to the Rust Manager")],
                    [sg.Button("1"), sg.Text("Signup (GUI) ")],
                    [sg.Button("2"), sg.Text("Login")],
                    [sg.Button("3"), sg.Text("Price Updater")],
                    [sg.Button("4"), sg.Text("Edit (dont forget to add remove) Favourites")],   
                ]
        Menu = sg.Window('Rust Manager', Menu, resizable=True, element_justification='l', location = (0, 0), )
        while cont == 0:
            events, Values = Menu.read()
            if events == '1':
                Menu.close()
                SignupGui()
                cont = 1
            elif events == '2':
                Menu.close()
                UserID = login()
                cont = 1
            elif events == '3':
                Menu.close()
                updater()
                cont = 1
            elif events == '4':
                Menu.close()
                if UserID != 'None':
                    bigloop = 0
                    while bigloop == 0:
                        favloop = 0
                        skins = Skins(connection)

                        Favs = [    [sg.Text("Favourites Manager")],
                        [sg.Button("1"), sg.Text("View Favourites (WIP)")],
                        [sg.Button("2"), sg.Text("Add Favourites")],
                        [sg.Button("3"), sg.Text("Remove Favourites(WIP)")],
                        [sg.Button("4"), sg.Text("Back to Menu")],   
                                ]
                        Favs = sg.Window('Favourites Manager', Favs, resizable=True, element_justification='l', location = (0, 0), )
                        while favloop == 0:
                            favevents, favValues = Favs.read()
                            if favevents == '1':
                                Favs.close()
                                favloop = 1
                            elif favevents == '2':
                                Favs.close()
                                favourites_add(skins, connection, UserID)
                                favloop = 1
                            elif favevents == '3':
                                Favs.close()
                                favloop = 1
                            elif favevents == '4':
                                Favs.close()
                                favloop = 1
                                bigloop = 1
                            elif favevents == sg.WINDOW_CLOSED:
                                Favs.Close()
                                favloop = 1
                                bigloop = 1
                    cont = 1
                else:
                    NoUserId = [ [sg.Text('UserID not found')],    #establishes layout for invalid username (taken)
                                [sg.Text('Please Login to Access Favourites')],
                                [sg.Button('Confirm')]  ]
                    
                    Failed = sg.Window('Please Login', NoUserId, resizable=True, element_justification='c', location = (0, 0)) #creates invalid window
                    close = 'n'
                    while close == 'n':
                        event3, values = Failed.read()
                        if event3 == 'Confirm': #checks if confirm pressed
                            close = 'y' 
                            Failed.close()
                        elif event3 == sg.WINDOW_CLOSED:    #checks if window closed
                            close = 'y'
                            Failed.close()
                    cont = 1
            elif events == sg.WINDOW_CLOSED:
                Menu.close()
                cont = 1
                choose = 'n'


def Skins(connection):
    with connection.cursor() as cursor:
        sql = "SELECT `skinname` from `rustskins`"
        test = cursor.execute(sql)
        rows = cursor.fetchall()
        skins = []
        for a in rows:
            b = a['skinname']
            skins.append(b)
        return skins
    

def favourites_add(skins, connection,UserID):
    sg.ChangeLookAndFeel('LightGrey1')   # Design Colour
    # Design of login screen
    fav = [  [sg.Text('Add to Favourites')],
                    [sg.Combo(skins)],
                    [sg.Button('Submit'), sg.Button('Cancel')],]
    window = sg.Window('Favourite Managed',fav)
    event, skin = window.read() 
    if event == 'Submit':
        skin = list(skin.values())
        skin = skin[0]
        with connection.cursor() as cursor:
                # Create a new record if all above criteria is met
                sql = "INSERT INTO `UserFav` (`User`, `Skin`) VALUES (%s, %s)"
                cursor.execute(sql, (UserID, skin))
        connection.commit() #commits to database
        window.close()
    else:
        window.close()
        return

connection = database_setup()
choose = 't'

mainline(choose)

# the join means wait untill it finished

#retrieve_password(connection)
icon_tag = 'https://community.akamai.steamstatic.com/economy/image/' #put icon url after this to retrieve i