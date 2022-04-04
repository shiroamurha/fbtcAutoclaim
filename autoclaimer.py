from playwright.sync_api import sync_playwright
from time import sleep
from datetime import datetime
import cookie_eater
import json



class Autoclaimer():

    def __init__(self):

        # deletes undesirable keys from cookie's dicts, also imports all the cookies from cookies.json
        self.cookies_ = cookie_eater.cookies_proccessing()
        
        # for counting the cicles of main loop
        self.iterator = 1
        one_hour = 61000*60 # actually not one hour, but one hour and one minute, for error margin


        # main worker loop, every 1 hour does the three methods in a row 
        while True:
            
            for _ in range(2): 

                # NOTE:
                # this loop runs claim management methods twice bc sometimes webkit can't resolve the url by timeout 
                # it is an already recognised bug of webdrivers that could be fixed by just setting wait_for_timeout()
                # with infinite time amount, but it could cause a lot of other issues like using "infinite" ram then
                # crashing the OS

                self.start_driver()
                exceptionRaised = self.claim() # returns True if exception is raised, else returns False
                self.close_driver()

                # if no exception is raised, then do this for loop only once
                if not exceptionRaised:
                    break
            
            self.iterator += 1

            with sync_playwright().start().webkit.launch().new_page() as p:
                p.wait_for_timeout(one_hour)
 

    def start_driver(self):
        
        # page and session (context) initiation

        self.playwright = sync_playwright().start() 
        self.browser = self.playwright.webkit.launch(ignore_default_args=["--mute-audio"])
        context = self.browser.new_context()
        self.page = context.new_page()


        # cookie adding management
        self.page.goto("https://freebitco.in/")

        context.add_cookies(self.cookies_)
        
        # after setting cookies, refreshes the page
        self.page.goto("https://freebitco.in/?op=home")

    ##

    def claim(self):

        last_log_info = open('log_info.txt', 'r').read()

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
                
            )

            roll_button.click()
            
        # if any exception occurs, write it on log_info.txt (normally timeout exception, 
        # explained on the note inside main worker loop at Autoclaimer().__init__())


        except Exception as e:
            
            open('log_info.txt', 'w').write(

                f"{last_log_info}\n{e} not able to detect button || at {self.date_now()}"
            )
            print(e, f'\n || at [{self.date_now()}]')

            return True
        
        else:
            #print(roll_button.text_content(), 'clicked!')

            open('log_info.txt', 'w').write(

                f"{last_log_info}\n claimed || at {self.date_now()}"
            )

            # breaks for loop of running methods twice if no exception is raised
            return False
    
    def close_driver(self):
        
        # logs on console the time that has been claimed
        print(f'[{self.date_now()}] claimed! >{self.iterator}< || waiting next')

        # closes browser and driver
        self.browser.close()
        self.playwright.stop()

    def date_now(self):

        date = str(datetime.now()) # gets only str from datetime.now()

        return date[0:19] # returns only 19 digits from date, that matches just year-month-day hour-minute-second (with no ms)



if __name__ == '__main__':
    
    # if code is running by its side, then calls autoclaimer class
    Autoclaimer()