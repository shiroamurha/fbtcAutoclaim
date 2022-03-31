from playwright.sync_api import sync_playwright
import json



class Autoclaimer():

    def __init__(self):
        
        self.start_driver()
        self.claim()

    def start_driver(self):
        
        # page and session (context) initiation 
        playwright = sync_playwright().start() 
        self.browser = playwright.webkit.launch()
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
        self.page.goto("https://freebitco.in/?op=home")

    ##

    def claim(self):
        
        try:
            play_without_captcha = self.page.dispatch_event(
            
                'div#play_without_captchas_button',
                'click'
            
            )
            
            roll_button = self.page.locator(
                
                'input[id="free_play_form_button"]'
                
            ).click()
            
        except Exception as e:
            print(e, ' not able to detect button')
        
        else:
            print(play_without_captcha, 'clicked!')
            
if __name__ == '__main__':
    Autoclaimer()