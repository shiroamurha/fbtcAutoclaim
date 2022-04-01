from playwright.sync_api import sync_playwright
from time import sleep
import json



class Autoclaimer():

    def __init__(self):
        
        # main worker loop, every 1 hour (3600sec) does the three methods in a row 
        while True:
            
            self.start_driver()
            self.claim()
            self.close_driver()
            
            sleep(3600)

    def start_driver(self):
        
        # page and session (context) initiation 
        self.playwright = sync_playwright().start() 
        self.browser = self.playwright.webkit.launch()
        context = self.browser.new_context()
        self.page = context.new_page()


        # cookie adding management
        self.page.goto("https://freebitco.in/")

        context.add_cookies(
            json.load(
                open(
                    'cookies.json', 
                    'r'
                )
            )
        )
        
        # after setting cookies, refreshes the page
        self.page.goto("https://freebitco.in/?op=home")

    ##

    def claim(self):
        
        # tries to roll without captcha 
        try:
            
            # sends directly the event of button's onclick 
            play_without_captcha = self.page.dispatch_event(
            
                'div#play_without_captchas_button',
                'click'
  
            )
            
            # roll click
            roll_button = self.page.locator(
                
                'input[id="free_play_form_button"]'
                
            ).click()
            
        # if any exception, breaks the code and then shows line with exception
        except Exception as e:
            print(e, ' not able to detect button')
        
        else:
            print(roll_button, 'clicked!')
    
    def close_driver(self):
        
        #closes browser and driver
        self.browser.close()
        self.playwright.stop()
        
        
            
if __name__ == '__main__':
    
    # if code is running by its side, then calls autoclaimer class
    Autoclaimer()