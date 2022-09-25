import cloudscraper
from bs4 import BeautifulSoup
import requests
import time
import smtplib, ssl
import datetime
import yfinance
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Trade():
    def __init__(self,symbol,SL,TP,pattern,direction,timeframe,tradeOpen):
        self.active = True
        self.timeOpen = datetime.datetime.now()
        self.timeClose = None
        self.symbol = symbol
        self.SL  =  SL
        self.TP  =  TP
        self.pattern = pattern
        self.direction = direction
        self.timeframe = timeframe
        self.open = tradeOpen
        self.PL = 0
        self.pips = 0
    def tpHit(self) -> str:
        self.timeClose = datetime.datetime.now()
        if(self.symbol.count("jpy")==0):
            self.pips = self.PL*1000
        else:
            self.pips = self.PL*100

        return self.symbol+" Timeframe "+self.timeframe+" Pattern "+self.pattern+" Hit TP for Profit of "+str(self.pips)+" pips"
    def slHit(self) -> str:
        self.timeClose = datetime.datetime.now()
        if(self.symbol.count("jpy")==0):
            self.pips = self.PL*1000
        else:
            self.pips = self.PL*100
        return self.symbol+" Timeframe "+self.timeframe+" Pattern "+self.pattern+" Hit SL for loss of "+str(self.pips)+" pips"
    


        


class Signals():
    
    def __init__(self):
        #TELEGRAM
        self.botToken = '5302796495:AAHgGwNVakRgMLeauCQvdI4FY5ULbZlv-_c'
        self.url = 'https://api.telegram.org/bot'+self.botToken+'/'
        self.chatid = '-1001638308883'

        #SELENIUM
        #self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.PATH = "/root/chromedriver"
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--shm-size=1g')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("enable-automation")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-browser-side-navigation")
        #chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = None#webdriver.Chrome(self.PATH,options=chrome_options)


        #triggerList = []
        self.firstrun = True
        self.tradeList = []
        self.scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    })

        self.body = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
                'Cookie' : 'logglytrackingsession=d9cab12c-b998-4d2b-ac5f-138496a4dd6c; G_AUTHUSER_H=0; adsFreeSalePopUp=1; adBlockerNewUserDomains=1649115065; gtmFired=OK; udid=464f355ddf2cd692530426c7f241cc2e; __cflb=02DiuGRugds2TUWHMkjZrtd2P76fwcs2iVqbeJYRuntFe; adbBLk=1; _gid=GA1.2.1747664679.1649115054; pms={"f":2,"s":2}; protectedMedia=2; G_ENABLED_IDPS=google; OB-USER-TOKEN=bc410a93-1b92-402a-954f-b1e724ca5d18; comment_notification_214859377=1; Adsfree_conversion_score=2; adsFreeSalePopUpee3723ddfdf0b2c76fcb8ade785f0ba4=1; r_p_s_n=1; PHPSESSID=jnq8ko3rnhk2qd96bhos2h1oer; geoC=US; smd=464f355ddf2cd692530426c7f241cc2e-1649179488; accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDkxODMzNzMsImp0aSI6IjIxNDg1OTM3NyIsImlhdCI6MTY0OTE3OTc3MywiaXNzIjoiaW52ZXN0aW5nLmNvbSIsInVzZXJfaWQiOjIxNDg1OTM3NywicHJpbWFyeV9kb21haW5faWQiOiIxIiwiQXV0aG5TeXN0ZW1Ub2tlbiI6IiIsIkF1dGhuU2Vzc2lvblRva2VuIjoiIiwiRGV2aWNlVG9rZW4iOiIiLCJVYXBpVG9rZW4iOiJaeWt5YzJacFpHeGhKV3BzWURFMU5qSm5NV0pqWVRFNk5EWm5ZemMzWlhNMElEVTdOR05tSUdWcU9YY3pNRFVwWWpZJTJCTjJWbE0yUTFORFJzT2pobk0yY3pNakptWkdRd1lUZHFNR0JpTlQ4eVl6RTRZMjB4TWpROVoyQTNNMlZuTkdZMVl6Um5aalZsTlRsaE0yZzFNbUp3UGlKbElUTWlOV2MwWkRwN1p5Qm5hREp6Wmpaa09tRXphalZnTkRWa01tUXhPR00zTVRBMFlHYzJOMlZsZlRSJTJGIiwiQXV0aG5JZCI6IiIsIklzRG91YmxlRW5jcnlwdGVkIjpmYWxzZSwiRGV2aWNlSWQiOiIiLCJSZWZyZXNoRXhwaXJlZEF0IjoxNjUxNjk5NzczfQ.1UveVELK8EBNxxnwJ96ciNFJIxiBPDMi_2Ea0NwMf88; pm_score=clear; panoramaId_expiry=1649784578804; _cc_id=3534f06993b6af01f8da6a9e694073ed; panoramaId=252c2513b68b780a009be012d8cc4945a702af13109fc36c25e3cd62edafb078; _hjSessionUser_174945=eyJpZCI6IjUzOTM2YWMyLTNiM2YtNTI1MC1hYmY2LThhYTYzNTA0NmQzNSIsImNyZWF0ZWQiOjE2NDkxNzk3NjUwMTAsImV4aXN0aW5nIjpmYWxzZX0=; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7fSwidXNlcklkIjoiMSJ9; _ga_H1WYEJQ780=GS1.1.1649179765.1.0.1649179774.51; _ga=GA1.2.1854034130.1649115054; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A4%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A2%3A%2215%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A22%3A%22Euro+Australian+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Feur-aud%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%224%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A21%3A%22US+Dollar+Swiss+Franc%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fusd-chf%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%228%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A28%3A%22New+Zealand+Dollar+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fnzd-usd%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%225%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A27%3A%22Australian+Dollar+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Faud-usd%22%3B%7D%7D%7D%7D; outbrain_cid_fetch=true; __cf_bm=Z.TgTJnoYMCvgJmDo0IL2IkxFFJiho_XZMuO68wF8ic-1649182410-0-AQlpaIZB+U43WcHlpR2I0ACzSDDpPMJRQV/9+XOB6fzpeNnmDF7Lq6yMWISmY9Jhy+XGeLemtXf9cxibILXBvb8qH1GJatLSASn2NZZHbOKDCV1lIsmE/nLe2cVaFFCfWUuvA8i/wgJfw1hEud7oeL7wnbJbf4eKHDFq/OHU9N9I; nyxDorf=OD9kMTJkZjs2amhlNW43YWA7YT42ODM5PT41PDQwM2w3MTZgYGw1MjA0OWJmPWRgMmEyMTNtOms2PzM3YzIyMjg6ZD0ybWZoNmloYg%3D%3D; invpc=17; _gat=1; _gat_allSitesTracker=1; ses_id=MX9mJzY5NT1iJjo8MGE3NDZjNmVmZGdsZWc0MDQ0YnRgdDY4ZTI0cmZpaCZnZGJ%2BY2MxNWMyYDVnNWZqM2VuPTE1Zmc2NjVpYmA6NTA3Nz02ZjZrZmlnN2VhNGI0ZWI%2BYGU2NWVmNGRmZWgxZ21iZWNxMS1jJ2BxZzVmNjNybikxPmYnNmY1a2IwOmUwazcyNm42bGZpZzBlbDQzNDNiemAr',
                'Referer' : 'https://www.investing.com/currencies/usd-chf-technical',
                'Upgrade-Insecure-Requests' : '1',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                'sec-ch-ua' : '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile' : '?0',
                'sec-ch-ua-platform' : '"Windows"'}
        self.headers = {'Accept' : '*/*', 
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Cookie' : 'adBlockerNewUserDomains=1658767674; udid=51a13288a1c2eed93624d5026c850b79; protectedMedia=2; _fbp=fb.1.1658767676283.2056109694; __gads=ID=b624cdbc6ff2eb63:T=1658767675:S=ALNI_MbFjvHpF2AhiPNVRq6xCRAeZIU8UQ; G_ENABLED_IDPS=google; _pbjs_userid_consent_data=3524755945110770; _cc_id=f20830b0ba50280ac106f2e593491b6b; _hjSessionUser_174945=eyJpZCI6IjU5OGRjM2E1LTc5ZDUtNTQ0ZC04OWI0LTE2OGMwZTVhMmVmMiIsImNyZWF0ZWQiOjE2NTg5MzgyNjU4MTQsImV4aXN0aW5nIjp0cnVlfQ==; r_p_s_n=1; pms={"f":2,"s":2}; pm_score=clear; _lr_env_src_ats=false; _ga_H1WYEJQ780=GS1.1.1662562775.3.1.1662562786.49.0.0; upa=eyJpbnZfcHJvX2Z1bm5lbCI6IiIsIm1haW5fYWMiOiI3IiwibWFpbl9zZWdtZW50IjoiMyIsImRpc3BsYXlfcmZtIjoiMTIxIiwiYWZmaW5pdHlfc2NvcmVfYWNfZXF1aXRpZXMiOiIzIiwiYWZmaW5pdHlfc2NvcmVfYWNfY3J5cHRvY3VycmVuY2llcyI6IjgiLCJhZmZpbml0eV9zY29yZV9hY19jdXJyZW5jaWVzIjoiOSIsImFjdGl2ZV9vbl9pb3NfYXBwIjoiMCIsImFjdGl2ZV9vbl9hbmRyb2lkX2FwcCI6IjAiLCJhY3RpdmVfb25fd2ViIjoiMSIsImludl9wcm9fdXNlcl9zY29yZSI6IjAifQ%3D%3D; geoC=US; comment_notification_214859377=1; Adsfree_conversion_score=3; adsFreeSalePopUpee3723ddfdf0b2c76fcb8ade785f0ba4=1; gtmFired=OK; __cflb=02DiuGRugds2TUWHMkkPH2QeWUbpq9vbTeNoakzWvBDoi; _gid=GA1.2.428120103.1663794565; __gpi=UID=000007be72bc997b:T=1658767675:RT=1663794565:S=ALNI_MazYFuiJsT0ih_0yE_DoHu955j6nA; _parrable_id=filteredUntil%253A1663880968%252CfilterHits%253A0; cto_bundle=nY_GaV9yMmhWVTJpZzVBSlp3ZEJTV2pDQjkzN3hQRG1waGdtWTg5Z3liOWl0ZUlOd0plV1NOU3hTcmxacmklMkYwTmt3QlZPbkpKVnR3OWZ2bzRVNzJ3TGpGcWI4ajJrT0FXUDhjaEU1VE9rUUI5cDZjNlVtV0pBeGdoZnZ4NlRNZjJyN2pxWjlIQ3JZRjNSbm9TQnVXOSUyQkhGalNBJTNEJTNE; cto_bidid=FAXeTF9takRZUGZFdm9QQlBMaTB6UjNudE8xbmNHb05mNUhJZTgwJTJGT0phTWdsWUtFaCUyRnRRNTgyNVZRSWRLN2dLUkRhZHp3SUVKc25Cb3dEV0h3NyUyRkl5OVhuZmhwaW10Y2YyZkRRZDBkdWxvNW0xbyUzRA; page_view_count=15; OptanonConsent=isIABGlobal=false&datestamp=Wed+Sep+21+2022+17%3A09%3A37+GMT-0400+(Eastern+Daylight+Time)&version=6.38.0&hosts=&consentId=4e69ea99-122d-4e88-9f20-8e2f092d8c09&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=US%3BMA; OptanonAlertBoxClosed=2022-09-21T21:09:37.028Z; pbjs-unifiedid=%7B%22TDID%22%3A%220773037d-4588-4d6c-86c3-0b5d1666136f%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-08-21T21%3A09%3A39%22%7D; pbjs-unifiedid_last=Wed%2C%2021%20Sep%202022%2021%3A09%3A39%20GMT; _ga_C4NDLGKVMK=GS1.1.1663794576.9.0.1663794601.35.0.0; _ga=GA1.2.952618519.1658767676; PHPSESSID=4iru24t16j740romun7igsp032; browser-session-counted=true; user-browser-sessions=4; smd=51a13288a1c2eed93624d5026c850b79-1663806630; __cf_bm=nTsZ6panb7RRK319U0j0cxmTlJ2ThzU11793wRALpQU-1663806632-0-AWZjRUmM/sbc5cI0cM7de7h+Xo0VBx1I/vW2CkDEURqwOxWFWrI0U7aYg8HrrFTIRJ67k3kPnu4Xw5Yxv2jOC8Lp0Dg0caiIKnvOszNBsqdBxqz5B8VPs6lNz+kKtfS5QDwr2BqzJ4gjjReKkYg1zUbZkS/+uwtiXw6fOPQkmdhs; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A7%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A2%3A%2213%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A24%3A%22Swiss+Franc+Japanese+Yen%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fchf-jpy%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%228%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A28%3A%22New+Zealand+Dollar+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fnzd-usd%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228839%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fus-spx-500-futures%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A2%3A%2247%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A33%3A%22Australian+Dollar+Canadian+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Faud-cad%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%221%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A14%3A%22Euro+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Feur-usd%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22945629%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A17%3A%22Bitcoin+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fcrypto%2Fbitcoin%2Fbtc-usd%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A2%3A%2248%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A29%3A%22Australian+Dollar+Swiss+Franc%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Faud-chf%22%3B%7D%7D%7D%7D; UserReactions=true; G_AUTHUSER_H=0; _lr_retry_request=true; panoramaId_expiry=1664411725558; panoramaId=46bf1cbd8511e75b0a36c3bfa8164945a702e8ecbfd3b02a602c8dac027b8797; invpc=5; outbrain_cid_fetch=true; ses_id=NngxcDQ7YWkzdz07NWRiYT9qM2A0NmVuZ2VjZzAwbngzJzc5YTY2cGFuPnAwM2R4PzsxNWFlZTIwZTI6ZGNvazYyMWM0MGFoMzY9MjVvYjM%2FZzNvNDdlZ2cwYzMwZm4wM2E3aGEyNjVhZz42MG9kPD8tMS1hJWV0MGIyYmQlbyg2OTFwNGRhPjNnPWM1N2I0PzgzPjRgZTVnY2NpMDZudjN4; nyxDorf=NjEwZWYwNGk0aDo3M2gyZGM4PmExP2JoMTJhaDUxNGtlYzNlYGw%2BMzNnYT9kZzgzPzowMzE0Zz82Yzc5Z2NkOTY5MDJmNzQ5NGQ%3D',
            'Origin' : 'https://www.investing.com',
            'Referer' : 'https://www.investing.com/currencies/eur-usd-technical',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'X-Requested-With' : 'XMLHttpRequest',
            'sec-ch-ua' : '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile' : '?0',
            'sec-ch-ua-platform' : '"Windows"',}

        self.periods = ['60','300','900','1800','3600','18000','86400','week','month']
        self.timeframes = {'15':'900',
                    '30':'1800',
                    '1H':'3600',
                    '5H':'18000',
                    '1D': '86400',
                    '1W' : 'week',
                    '1M' : 'month'}
        self.symbolDict = {'usd-chf' : 4,
                'usd-cad' : 7,
                'nzd-usd' : 8,
                'eur-aud' : 15,
                'aud-usd' : 5,
                'usd-jpy' : 3,
                'eur-cad' : 16,
                'eur-usd' : 1,
                'aud-cad' : 47,
                'aud-chf' : 48,
                'aud-jpy' : 49,
                'aud-nzd' : 50,
                'cad-chf' : 14,
                'cad-jpy' : 51,
                'chf-jpy' : 13,
                'eur-chf' : 10,
                'eur-gbp' : 6,
                'eur-jpy' : 9,
                'gbp-aud' : 53,
                'gbp-cad' : 54,
                'gbp-chf' : 12,
                'gbp-jpy' : 11,
                'gbp-usd' : 2,
                'nzd-cad' : 56,
                'nzd-jpy' : 58,
                'nzd-usd' : 8} 
    
    

    def getTechnicalVerification(self,symbol:str,direction:str,timeframe:str) -> bool:
        print("Checking "+symbol+" "+direction+" On "+timeframe)
        #Timeframe to period
        
       #"https://www.investing.com/currencies/"+symbol+"-technical",headers=self.headers)
        self.driver.get("https://www.investing.com/currencies/"+symbol+"-technical")
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        text = soup.find_all("div",{"class":"summaryTableLine"})[1].text.upper()
        #self.driver.close()
        if(direction=="SELL" and text.count("SELL") == 2 or direction == "BUY" and text.count("BUY")  ==  2):
            return True
        else:
            return False
            
        
    def getTPSL(self,symbol:str,direction:str,timeframe) -> tuple:
        

        self.driver.get("https://www.investing.com/currencies/"+symbol+"-technical")
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        list = soup.find_all('td',{"class": "right"})
        
        price = float(soup.find_all('span',{"id": "last_last"})[0].text)

        atr = float(list[7].text)
        #self.driver.close()
        if(direction == "BUY"):
                return (round((price-atr),5),round((price+atr),5))
        else:
                return (round((price+atr),5),round((price-atr),5))



    def getVolatility(self, symbol:str, timeframe:str) -> bool:
        
            
        data = {'pairID':self.symbolDict[symbol],
            'period':self.timeframes[timeframe],
            'viewType':'normal'}

        html = self.scraper.post("https://www.investing.com/instruments/Service/GetTechincalData",headers=self.headers,data=data)#https://www.investing.com/instruments/Service/GetTechincalData?pairID=4&period=86400&viewType=normal


        if(html.text.count("Less Volatility")>=1):
            return True
        else:
            return False

    #Hits investing.com endpoint to grab list of candlestick patterns on symbol
    def getCandlestickSignal(self,symbol: str) -> None: 
        #self.scraper = cloudscraper.create_scraper()
        
        #https://www.investing.com/currencies/eur-usd-candlestick
        html = self.scraper.get("https://www.investing.com/currencies/"+symbol+"-candlestick",data = self.body).text
        
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')

        
        for pattern in soup.find_all('tr'):
                #High Probability Patterns that are Current or 1 bar old
                if(str(pattern).count('title="High"')==1 and (pattern.find_all('td')[4].text == "Current" or int(pattern.find_all('td')[4].text) <= 1)): #modified current to get more reliable signals (pattern.find_all('td')[4].text == "Current" or 
                        timeframe = pattern.find_all('td')[2].text
                        trigger = timeframe+symbol+str(pattern.find_all('td')[4].text)+'month:'+str(datetime.datetime.now().month)+'day:'+str(datetime.datetime.now().day)
                        file = open('trigger.txt','r')
                        if(file.read().count(trigger)==1):
                            continue
                        file.close()
                        
                        if(timeframe == '15'  or timeframe == '30' or timeframe == '1M'):
                            print('Failed timeframe check')
                            continue

                        direction = ""
                        if(str(pattern).count('bullRevIcon') or str(pattern).count('bullContIcon')):
                                direction = 'BUY'
                        elif(str(pattern).count('bearRevIcon') or str(pattern).count('bearContIcon')):
                                direction = 'SELL'
                        else:
                            print("Failed to find direction")
                            continue
                        #Check trend
                        if(self.getTechnicalVerification(symbol,direction,timeframe)):#self.getVolatility(symbol,timeframe) and 
                                #CREATE ORDER
                                print("Take Trade: "+symbol+" Pattern: "+pattern.find_all('td')[1].text+" Direction: "+direction+" Timeframe: "+timeframe)
                                tpsl = self.getTPSL(symbol,direction,timeframe)
                                file = open('trigger.txt','a')
                                file.write(trigger)
                                #triggerList.append(trigger)
                                print(tpsl)
                                try:
                                    tradeOpen = yfinance.Ticker(symbol.replace("-","")+"=X").info['ask']
                                    self.tradeList.append(Trade(symbol,tpsl[0],tpsl[1],pattern.find_all('td')[1].text,direction,timeframe,tradeOpen))
                                    message = "Take Trade: "+symbol+" Pattern: "+pattern.find_all('td')[1].text+" Direction: "+direction+" Timeframe: "+timeframe+" TPSL: "+str(tpsl)+" Trade Open"+str(tradeOpen)
                                    requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+message)
                                    #sendImageurl='https://www.fxstreet.com/rates-charts/chart-interactive?asset='+symbol.replace('-','')
                                    
                                except:
                                    print("email failure")
    
    #Prevents calls from being made during off market hours
    def marketHours(self) -> bool:
        if((datetime.datetime.now().weekday()==4 and datetime.datetime.now().hour > 17) or datetime.datetime.now().weekday()==5 or datetime.datetime.now().weekday()==6 and datetime.datetime.now().hour < 17):
            return False
        return True

    #Checks trades vs current price to send telegram notif
    def checkTrades(self) -> None:
        for trade in self.tradeList:
            if(trade.active):
                pair = yfinance.Ticker(trade.symbol.replace("-","")+"=X")
                currentPrice = (pair.info['ask'] + pair.info['bid'])/2
            if(trade.direction == "BUY"):
                if(currentPrice<trade.SL):
                    trade.active = False
                    trade.PL = -1*abs(trade.open-trade.SL)
                    requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+trade.slHit())
                if(currentPrice>trade.TP):
                    trade.active = False
                    trade.PL = abs(trade.open-trade.SL)
                    requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+trade.tpHit())
            if(trade.direction == "SELL"):
                if(currentPrice>trade.SL):
                    trade.active = False
                    trade.PL = -1*abs(trade.open-trade.SL)
                    requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+trade.slHit())
                if(currentPrice<trade.TP):
                    trade.active = False
                    trade.PL = abs(trade.open-trade.SL)
                    requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+trade.tpHit())
    
    #Returns Weekly Summmary from self.tradeList 
    def weeklySummary(self) -> None:
        winCount = 0
        lossCount = 0
        totalPips = 0
        unrealizedTrades = 0
        for trade in self.tradeList:
            if(not trade.active and trade.timeClose > datetime.datetime.now() - datetime.timedelta(days=5)):
                if(trade.pips<0):
                    lossCount+=1
                else:
                    winCount+=1
                totalPips += trade.pips
            if(trade.active):
                unrealizedTrades += 1

        message =  "           Weekly Summary           \n Total Loosers: "+str(lossCount)+"\n Total Winners:  "+str(winCount)+"\n Win Rate: "+str(winCount/(lossCount+winCount))+"\n Total Pips: "+str(totalPips)+"\n Open Trades: "+str(unrealizedTrades)
        requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+message)

    #LOOP FUNCTION
    def main(self):
        
        while True:
            #Market Open
            if(datetime.datetime.now().weekday()==6 and datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 0):
                message = "-------Market Open!-------"
                requests.get(self.url+'sendMessage?chat_id='+self.chatid+'&text='+message)
            #End of Market
            if(datetime.datetime.now().weekday()==4 and datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 0):
                self.weeklySummary()
                time.sleep(60)
            #Reset Trigger List
            if(datetime.datetime.now().hour == 12 and datetime.datetime.now().minute == 0):
                print('12pm')
                #triggerList = []
            #Ran every 15 minutes check current candlestick patterns
            if(self.marketHours() and datetime.datetime.now().minute%15==0 or self.firstrun):
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=self.chrome_options)
                for symbol in self.symbolDict:
                    try:      
                       self.getCandlestickSignal(symbol)
                    except Exception as e:
                        print("ERROR MESSAGE")
                        print(e)
                        time.sleep(60)
                
                self.driver.quit()
                print("Running Checks")
                self.firstrun = False
                self.checkTrades()
                time.sleep(60)
            else:
                print("Not Market Hours")
                time.sleep(60)



signal = Signals()
signal.main()