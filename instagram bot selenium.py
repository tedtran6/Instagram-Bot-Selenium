from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

class InstagramBot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

        option = webdriver.ChromeOptions()
        #option.add_argument('headless')

        self.driver = webdriver.Chrome(r"C:\Users\Ted\AppData\Roaming\SPB_Data\Selenium Web Drivers\chromedriver.exe", options=option)
        self.shorter_total_followed = 0
        self.total_followed = 0
        self.times_restricted = 0
        self.restricted = False
        
    def closeBrowser(self):
        self.driver.close()
        
    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        
        time.sleep(2)
        
        #this input is so sensitive that if you accidentially give it a forwardslash that doesn't exist, it will have an error. 
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
            #<a href="/accounts/login/?source=auth_switcher">Log in</a>
            # "a[@href'accounts/login/?source=auth_switcher']"
        
        #remember to add sleep time!!
        time.sleep(2)
        
        #NAMEs
        #input user name: username
        username_elem = driver.find_element_by_xpath("//input[@name='username']")
        username_elem.click()
        username_elem.send_keys(self.username)
        
        #input password name: password
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.click()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.ENTER)
        
        time.sleep(4)

        #<button class="aOOlW   HoLwm " tabindex="0">Not Now</button>
        #only the "HoLwm" part
        try:
            driver.find_element_by_class_name("HoLwm").click()              #headless can't find this button. This button is the 
        except Exception:
            print("there is no notifiaction button.")

    #if you are already logged in to instagram, log out.
    def logout(self):
        driver = self.driver
        time.sleep(2)
        try:
            self_button = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[3]/a")
            self_button.click()
            time.sleep(1)
            options_button = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/button/span")
            options_button.click()
            time.sleep(1)
            logout_button = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/button[6]")
            logout_button.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

    #like all photos in the explore page of one hashtag
    def like_photo_explore(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        #scroll down
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        #find links for every single instagram page
        #REMEMBER TO USE ELEMENTS WITH AN ****S*****
        hrefs = driver.find_elements_by_tag_name('a')
        #compact for loop retrives ONLY hrefs of the element list and puts into another list.
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]

        #idk what this does, but it gets rid of a lot of results "cleaning links"
        #pic_hrefs = [href for href in pic_hrefs if hashtag in href]
        print(hashtag + ' photos: ' + str(len(pic_hrefs)))

        #make this into a helper function
        
        #<span class="glyphsSpriteHeart__outline__24__grey_9 u-__7" aria-label="Like"></span>

        for pic_href in pic_hrefs:
            driver.get(pic_href)    #go to the link
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #you can just copy Xpath from chrome
            try:
                driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/section[1]/span[1]/button/span").click()
                time.sleep(18)          #18 second wait about 200 likes per hour
            except Exception as e:
                time.sleep(2)
                print("exception")

    #not done yet
    def like_photo_explore_comments(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        #scroll down
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        hrefs = driver.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]

        print(hashtag + ' photos: ' + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)    #go to the link
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #LOAD ALL COMMENTS
            more_comments_xpath = "//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button"

            button_exists = self.element_exists_xpath(more_comments_xpath)
            while(button_exists):
                try:
                    driver.find_element_by_xpath(more_comments_xpath).click()
                    time.sleep(0.20)
                    button_exists = self.element_exists_xpath(more_comments_xpath)
                except Exception:
                    time.sleep(1)

    #makes you wait longer and longer times the more we are restricted. 
    def restriction_punishment(self):
        self.logout()
        print("logged out")
        #wait 12 hours plus some random amount of time from 1 hour to 3 hours. 
        time_to_rest = 43200 + random.randint(3600, 10800)
        print("generated time to rest")
        print("time to rest after restriciton: " + str(time_to_rest) + " #######################################")
        time.sleep(time_to_rest)
        self.login()

    #follow the user given in the href and like their most recent photo. 
    #INPUT:
    #href: the link for the user to follow
    def follow_user(self, href):
        print("trying to follow new user")
        driver = self.driver
        user_open_script = "window.open('" + str(href) + "', 'new window')"
        driver.execute_script(user_open_script)
        driver.switch_to_window(driver.window_handles[1])
        time.sleep(0.5)

        #to prevent us from trying to follow an account we've already followed, which happens a lot. 
        #if it is a public account, and I've already followed it... already_followed = True
        already_followed = True
        is_public = True
        try:
            if driver.find_element_by_class_name("yZn4P").text == "Following":
                already_followed = True
            else:
                already_followed = False
            is_public = True
        except Exception:
            is_public = False

        try:
            if is_public == False:
                if(driver.find_element_by_class_name("L3NKy").text == "Requested"):
                    already_followed = True
                else:
                    already_followed = False
        except Exception:
            already_followed = False

        #if I haven't already clicked follow on the account...
        if not already_followed:
            new_follow = True
            #if follow button is displayed...
            #follow a public account
            try:
                if driver.find_element_by_class_name("yZn4P").is_displayed():
                    follow_button = driver.find_element_by_class_name("yZn4P")
                    follow_button.click()   #click the follow button.
                    time.sleep(2)
                    button_after_text = follow_button.text
                    if(button_after_text == "Follow"): #wait if limit hit
                        self.restricted = True
                        new_follow = False
                        print("Restricted, wait 20 minutes")
                        time.sleep(1)
                        self.restriction_punishment()
                    else:
                        self.restriced = False

                        self.like_first_picture(href)   #if we can follow the user, also like their first picture.
                    #JUST IN CASE if we already followed the user, click cancel. Not needed anymore because we already checked earlier.
                    try:
                        if driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[3]/button[2]").is_displayed():
                            driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[3]/button[2]").click()
                            new_follow = False
                    except Exception:
                        time.sleep(1)
                    
                    time.sleep(0.2)
                else:
                    print("not followed")
            except Exception:
                is_public = False
                print("acount is not public")

            #follow a private account
            if is_public == False:
                try:
                    if driver.find_element_by_class_name("L3NKy").is_displayed():
                        follow_button = driver.find_element_by_class_name("L3NKy")
                        follow_button.click()   #click the follow button.
                        time.sleep(2)
                        button_after_text = follow_button.text
                        if(button_after_text == "Follow"): #wait if limit hit
                            self.restricted = True
                            new_follow = False
                            print("Restricted, wait 20 minutes")
                            time.sleep(1)
                            self.restriction_punishment()
                        else:
                            self.restricted = False
                        #JUST IN CASE, if we already followed the user, click cancel. Not needed really because we already checked earilier 
                        try:
                            if driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[3]/button[2]").is_displayed():
                                driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[3]/button[2]").click()
                                new_follow = False
                        except Exception:
                            time.sleep(1)
                        
                        time.sleep(0.2)
                    else:
                        print("not followed")
                except Exception:
                    time.sleep(1)

        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        return new_follow


        #like commenters of photos in a popular instagram account
    
    #likes all the commenters who tagged their friends on ONE photo.
    #INPUT:0
    #href: href of a single picture
    #time_between_follows: time before the next follow occurs.
    #followed_counter: number of people already followed recently before this method
    #time_burst_interval: the time it takes for the next burst of follows to begin  [10-15 minutes (600s - 900s)]
    #burst_follows: number of accounts to follow before the burst wait time.        [40 acocunts (neutrino style)]
    #ADD: burst interval, burst follows.

    def follow_commenters_one_picture(self, href, time_between_follows, followed_counter = 0, burst = False, time_burst_interval = 0, burst_follows = 0):

        driver = self.driver
        driver.get(href)
        time.sleep(2)
        
        #LOAD ALL COMMENTS
        more_comments_xpath = "//*[@id='react-root']/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button"

        button_exists = self.element_exists_xpath(more_comments_xpath)
        #limit the number of times we look for more comments on the page
        button_clicks = 0
        while(button_exists and button_clicks < 30):
            try:
                driver.find_element_by_xpath(more_comments_xpath).click()
                time.sleep(0.20)
                button_exists = self.element_exists_xpath(more_comments_xpath)
                button_clicks += 1
            except Exception:
                time.sleep(1)

        #only use the last part of the class name. 
        #comm = driver.find_elements_by_class_name('TlrDj')

        comm = driver.find_elements_by_class_name('C4VMK')
        print("total # of commenters: " + str(len(comm)))
        for commenter in comm:
            if self.restricted == True:      #if we are restricted, don't go through all of the comments. 
                break
            time.sleep(0.2)

            person_commenting = commenter.find_element_by_class_name('_6lAjh').find_element_by_class_name('TlrDj')
            print(person_commenting.get_attribute('href'))
            try:
                comment_text = commenter.find_element_by_tag_name('span').find_element_by_tag_name('a')
                print(comment_text.get_attribute("text"))
                comment_str = comment_text.get_attribute("text")
                if "@" in comment_str:  #if they tagged a friend...
                    #check if they tagged themselves.
                    if(person_commenting.get_attribute('href') != comment_text.get_attribute('href')):
                        #FOLLOW THE COMMENTER
                        if self.follow_user(person_commenting.get_attribute('href')):     #if you followed new person...
                            print("TEST TO SEE IF FOLLOWED NEW USER")
                            followed_counter += 1
                            self.shorter_total_followed += 1
                            self.total_followed += 1
                            print("Users followed in burst cycle : " + str(followed_counter))
                            print("Shorter Total followed        : " + str(self.shorter_total_followed))
                            print("Total Users followed          : " + str(self.total_followed) + " ########################")
                            time.sleep(time_between_follows)

                            if(self.shorter_total_followed > 399):
                                print("longer sleep after 399 follows, for about 12 hours + ##############")
                                print("NOT ACTUALLY RESTRICTION")
                                self.shorter_total_followed = 0
                                self.restriction_punishment()

                            #if we are bursing follows, and followed counter >= burst_follows limit...
                            if(burst and followed_counter >= burst_follows):
                                print("burst sleep for " + str(time_burst_interval) + "s")
                                time.sleep(time_burst_interval)                 #sleep for a long time... about 10-15 minutes?
                                followed_counter = 0                            #reset the followed counter
                            time.sleep(0.5)
                    else:
                        print("did not follow, user tagged themselves.")

            except Exception as e:
                time.sleep(.1)
                print("NO TAG")

        return(followed_counter)

    def follow_commenters_one_account(self, href, time_between_follows, followed_counter = 0, burst = False, time_burst_interval = 0, burst_follows = 0):
        driver = self.driver
        driver.get(href)
        time.sleep(2)

        #change it to allow function to display longer or shorter amounts. 
        #scroll down
        for i in range(1, 5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        #scroll back up
        driver.execute_script("window.scrollTo(0, 0);")

        #only picture elements in the page
        hrefs = driver.find_element_by_class_name(' _2z6nI').find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]

        print('Account Photos Displayed: ' + str(len(pic_hrefs)))
    
        for pic_href in pic_hrefs:
            if self.restricted == True:     #if we are restricted, stop going through the accounts pictutures. 
                break
            followed_counter = self.follow_commenters_one_picture(pic_href, time_between_follows, followed_counter, burst, time_burst_interval, burst_follows)
    
    #unique from follow_commenters_one_account because it will move on to a new account when we are restricted.
    def follow_commenters_multiple_accounts(self, account_hrefs, time_between_follows, followed_counter = 0, burst = False, time_burst_interval = 0, burst_follows = 0):
        #for every single account href in the list...
        i = 0
        while i < 4:
            for account_href in account_hrefs:
                self.follow_commenters_one_account(account_href, time_between_follows, followed_counter, burst, time_burst_interval, burst_follows)
            #if we get restricted along the way, increment the times restricted. If everything went fine for one account, reset the restriction counter.
                if self.restricted == True:
                    self.times_restricted += 1
                else:
                    self.times_restricted = 0
                self.restricted = False
            i += 1

    #likes the most recent picture picture in the account
    def like_first_picture(self, href):
        driver = self.driver
        driver.get(href)    #go to the users page

        time.sleep(2)

        hrefs = driver.find_element_by_class_name(' _2z6nI').find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]

        driver.get(pic_hrefs[0])    #go to the first link
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #you can just copy Xpath from chrome
        try:
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/section[1]/span[1]/button/span").click()
            time.sleep(1)
        except Exception:
            time.sleep(2)
            print("exception")

    #checks if the element is there by xpath.
    def element_exists_xpath(self, xpath):
        driver = self.driver
        try:
            driver.find_element_by_xpath(xpath)
            return True
        except Exception:
            return False


mybot = InstagramBot("insert your username", "insert your password")
mybot.login()

#log out of the account
#mybot.logout()

#testing restriction log out
#mybot.restriction_punishment()

#liking the first picture of an account
#mybot.like_first_picture("https://www.instagram.com/teslamotors/")

#following one user
#follow a public account
#print(mybot.follow_user("https://www.instagram.com/lamborghini/"))

#closest 1
#mybot.follow_commenters_one_picture("https://www.instagram.com/p/BqdSVQwnB4N/", 60)

#mybot.like_photo_explore_comments("humor")

#like all commenters of many posts in one page
#page, # seconds before next follow
#once every 60 seconds stopped me.
#mybot.follow_commenters_one_account("https://www.instagram.com/memezar/", 90)

#trying the burst function

#I could not follow anymore after 40 follows
#2 CLOSEST
#will not work well long term. Need to build a list of pages to follow and then switch between them evey time there is an error
#mybot.follow_commenters_one_account("https://www.instagram.com/memezar/", 1, followed_counter = 0, burst = True, time_burst_interval = 700, burst_follows = 35)

popular_accounts = ["https://www.instagram.com/memes/", "https://www.instagram.com/vines/",
                    "https://www.instagram.com/funnyordie/", "https://www.instagram.com/__memesfordays____/", 
                    "https://www.instagram.com/comedy.xo/"]

#3 closest
mybot.follow_commenters_multiple_accounts(popular_accounts, 1, followed_counter = 0, burst = True, time_burst_interval = 700, burst_follows = 35)

#target_hashtags = ['funny', 'memes', 'meme', 'lol']
#[mybot.like_photo_explore(tags) for tags in target_hashtags]    #another compact for loop

print("no failures")
