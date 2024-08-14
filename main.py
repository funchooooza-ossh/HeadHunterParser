#code by funchooooza-ossh. Good luck dude ;)
import time
from multiprocessing.pool import Pool
import re
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from driver import ChromeDriver
from srcapper import Scrapper



def main():     
    print("#code by funchooooza-ossh. Good luck dude ;)")
    start=time.perf_counter()
    driver = ChromeDriver.get_chromedriver(use_proxy=False,user_agent=True,headless=True)
    url=input('Input your url\nYou can tune your own filters in your browser, then input url to vacancies pool\n')
    driver.get(url)

    count = driver.find_element(By.XPATH,'.//h1').get_attribute('outerHTML')
    count = BeautifulSoup(count,'lxml').getText(strip=True)
    count=re.split(r'[в]',count)[0]
    count=''.join(count.split())
    count=int(count)

    print(f'Vacancies catched:{count} vacancies')

    pages=Scrapper.page_count(driver)
    print(f'Total pages:{pages}\nStart parsing...')
    driver.close()
    driver.quit()

    urls=Scrapper.url_list(url,pages)
    process_count=input('Input process count: \nProcces count is a count of chrome-drivers working at the same time \n')

    if pages>1:
        for ur in urls:
            href_list=Scrapper.getpage(ur)
            try:
                
                p=Pool(processes=int(process_count))
                print(f'Starting with {process_count} processes\n')
                p.map(Scrapper.scrap,href_list)
            except Exception as ex:
                print (ex)
                     
                
    else:
        urls=Scrapper.getpage(url)
        p=Pool(processes=int(process_count))
        print(f'Starting with {process_count} processes\n')
        p.map(Scrapper.scrap,urls)
         
    finish=time.perf_counter()

    print('Work time: '+str(finish-start))
    
    


if __name__ == '__main__':
    main()

