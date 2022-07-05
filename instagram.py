from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class Instagram:
    def __init__(self,nickname,password,code):
        self.nickname=nickname
        self.password=password
        self.code=code
        
        self.website="https://www.instagram.com/"

        self.options = Options()
        self.options.add_argument('--headless')

        self.timeout=5
        self.driver=webdriver.Firefox(options=self.options)

        self.followerList=[]
        self.followingList=[]
        self.followingButUnfollower=[]
        self.followerButUnfollowing=[]

    def Login(self):
        
        self.driver.get(self.website)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass

        nickNameInput=self.driver.find_element(by=By.XPATH,value='//*[@id="loginForm"]/div/div[1]/div/label/input')
        passwordInput=self.driver.find_element(by=By.XPATH,value='//*[@id="loginForm"]/div/div[2]/div/label/input')

        nickNameInput.send_keys(self.nickname)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass
        
        action=webdriver.ActionChains(self.driver)
        if self.code!="":
            for i in range(3):
                try:
                    secondPasswordInput=self.driver.find_element(by=By.XPATH,value='//section/main/div/div/div[1]/div/form/div[1]/div/label/input')
                    
                    secondPasswordInput.send_keys("")
                    action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()

                    secondPasswordInput.send_keys(self.code)

                    secondPasswordInput.send_keys(Keys.ENTER)
                    try:
                        element_present = EC.presence_of_element_located((By.ID, 'main'))
                        WebDriverWait(self.driver, self.timeout).until(element_present)
                    except TimeoutException:
                        pass
                except:
                    pass
                        
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass

    def IsLogggedIn(self):
        self.GoProfile()
        try:
            txt=self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/section/main/div/header/section/div[1]/div/div/div/button/div").text
        except:
            try:
                txt=self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[1]/div/a").text
            except:
                txt=""
        
        if txt=="Follow":
            return False
        elif txt=="Edit profile":
            return True
        else:
            return False
        
    def GoProfile(self,selection=0):
        if selection==0:
            self.websiteProfile="https://www.instagram.com/"+self.nickname+"/"
            
            self.driver.get(self.websiteProfile)
        elif selection==1:
            self.websiteProfile="https://www.instagram.com/"+self.nickname+"/followers/"
            
            self.driver.get(self.websiteProfile)
        elif selection==2:
            self.websiteProfile="https://www.instagram.com/"+self.nickname+"/following/"
            
            self.driver.get(self.websiteProfile)
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass

    def GetFollower(self):
        self.GoProfile(selection=1)

        action=webdriver.ActionChains(self.driver)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass

        dialogBox=self.driver.find_element(by=By.CSS_SELECTOR, value="div[role=dialog] ul")
        data=dialogBox.find_elements_by_css_selector("li")
        followerLen=len(data)
        
        k=0
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()

        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass
        
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()

        
        while True:
                        
            action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
                WebDriverWait(self.driver, self.timeout).until(element_present)
            except TimeoutException:
                pass
            data=dialogBox.find_elements_by_css_selector("li")
            if followerLen==len(data):
                k+=1
                time.sleep(0.125)
            else:
                k=0
                followerLen=len(data)
                try:
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
                    WebDriverWait(self.driver, self.timeout).until(element_present)
                except TimeoutException:
                    pass
            if k>=4:
                break
           
        data=dialogBox.find_elements_by_css_selector("li")
        for user in data:
            user=user.text.split("\n")
            nick=user[0]
            name=user[1]
            if name=="Remove" or name=="Verified" or name=="·" or name=="Follow" or name==".":
                name="Null"
            temp=[]
            temp.append(nick)
            temp.append(name)
            self.followerList.append(temp)
                
    def GetFollowing(self):
        self.GoProfile(selection=2)

        action=webdriver.ActionChains(self.driver)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass
        dialogBox=self.driver.find_element(by=By.CSS_SELECTOR, value="div[role=dialog] ul")
        data=dialogBox.find_elements_by_css_selector("li")
        followingLen=len(data)
        
        k=0
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()

        
        while True:
            
            action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            
            action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            
            action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
                WebDriverWait(self.driver, self.timeout).until(element_present)
            except TimeoutException:
                pass
            data=dialogBox.find_elements_by_css_selector("li")
            if followingLen==len(data):
                k+=1
                time.sleep(0.125)
            else:
                k=0
                followingLen=len(data)
                try:
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
                    WebDriverWait(self.driver, self.timeout).until(element_present)
                except TimeoutException:
                    pass
            if k>=4:
                break
   
        data=dialogBox.find_elements_by_css_selector("li")    
        count=1
        for user in data:
            user=user.text.split("\n")
            nick=user[0]
            name=user[1]
            if name=="Remove" or name=="Verified" or name=="Following" or name=="·" or name==".":
                name="Null"
            temp=[]
            temp.append(nick)
            temp.append(name)
            self.followingList.append(temp)

    def Logout(self):
        self.driver.get(self.websiteProfile)
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass
        self.driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span').click()
        
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'rq0escxv l9j0dhe7 du4w35lb'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass

        self.driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/div[2]').click()

    def FindDifference(self):
        for user in self.followingList:
            if user not in self.followerList:
                self.followingButUnfollower.append(user)
        

        for user in self.followerList:
            if user not in self.followingList:
                self.followerButUnfollowing.append(user)
            

