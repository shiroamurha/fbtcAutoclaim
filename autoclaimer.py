from playwright.sync_api import sync_playwright
from time import sleep
import cookie_eater
import json



class Autoclaimer():

    def __init__(self):

        # deletes undesirable keys from cookie's dicts, also imports all the cookies from cookies.json
        self.cookies_ = cookie_eater.cookies_proccessing()
        
        iterator = 1
        
        # main worker loop, every 1 hour (3600sec) does the three methods in a row 
        while True:
            
            for _ in range(2): 

                # NOTE:
                # this loop runs claim management methods twice bc sometimes webkit can't resolve the url by timeout 
                # it is an already recognised bug of webdrivers that could be fixed by just setting wait_for_timeout()
                # with infinite time amount, but it could cause a lot of other problems like using "infinite" ram then
                # crashing the OS

                self.start_driver()
                self.claim()
                self.close_driver()

            print(f'claimed! >{iterator}< || waiting next', end='')
            iterator += 1

            for _ in range(4):

                sleep(925) # (3700) plus 100sec bc driver sometimes (?????) is async
                print('.', end='') # print one dot on the other print above every 1/4 hour (900sec + 25sec from error margin)


            print() # just \n 

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
            open('log_info.txt', 'w').write(f"{open('log_info.txt', 'r').read()}\n{e} not able to detect button")
            print(e)
        
        else:
            #print(roll_button.text_content(), 'clicked!')
            pass
    
    def close_driver(self):
        
        #closes browser and driver
        self.browser.close()
        self.playwright.stop()
        
        
            
if __name__ == '__main__':
    
    # if code is running by its side, then calls autoclaimer class
    Autoclaimer()