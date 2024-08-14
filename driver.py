import random
import os
import fake_useragent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('.','.env')
load_dotenv(dotenv_path)

class ChromeDriver:
    def get_chromedriver(use_proxy=False, user_agent=None,headless=True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--accept-ssl-certs')
        chrome_options.add_argument('--start-maximized')
        
        if use_proxy:
            
            proxylist=[
            os.getenv("PROXY1"),
            os.getenv("PROXY2"),
            os.getenv("PROXY3")
            ]
                
            proxy=random.choice(proxylist)

            PROXY_HOST = proxy.split(':')[0]
            PROXY_PORT = proxy.split(':')[1]
            PROXY_USER = os.getenv("PROXY_USER")
            PROXY_PASS = os.getenv("PROXY_PASS")
            
            chrome_options.add_argument(f'--proxy-server={proxy}')
        

        if user_agent:
            user_agent=fake_useragent.UserAgent().random
            chrome_options.add_argument(f'--user-agent={user_agent}')

        if headless:
            chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        return driver