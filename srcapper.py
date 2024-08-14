#code by funchooooza-ossh. Good luck dude ;)
from driver import ChromeDriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from database import db
class Scrapper:
    def getpage(url):
        driver = ChromeDriver.get_chromedriver(use_proxy=False,user_agent=True, headless=True)
        driver.get(url)

        hrefs = driver.find_elements(By.XPATH,'//*[@id="a11y-main-content"]//h2/span/a')
                
        href_list = []
        for href in hrefs:
            href = href.get_attribute('href')
            href_list.append(href)

        href_list = list(set(href_list))
        driver.close()
        driver.quit()
        return href_list

    def scrap(url):
        driver = ChromeDriver.get_chromedriver(use_proxy=False, user_agent=True, headless=True)
        driver.get(url=url)           
        try:
            name = driver.find_element(By.CSS_SELECTOR,'[data-qa="vacancy-title"]').get_attribute('outerHTML')
            name = Scrapper.prettify(name)
            
            try:
                salary = driver.find_element(By.CSS_SELECTOR,'[data-qa="vacancy-salary"]').get_attribute('outerHTML')
                salary=Scrapper.prettify(salary)
                 
            except:
                salary='Salary not presented'
                
            company = driver.find_element(By.CLASS_NAME,'vacancy-company-name').get_attribute('outerHTML')
            company = Scrapper.prettify(company)
            
            location_strategies = [
                (By.CSS_SELECTOR, '[data-qa="vacancy-view-location"]'),
                (By.CSS_SELECTOR, '[data-qa="vacancy-view-raw-address"]')
            ]
            for strategy in location_strategies:
                found = False
                try:
                    location = driver.find_element(*strategy).get_attribute('outerHTML')
                    location = Scrapper.prettify(location)
                    found = True

                except: 
                    pass

                finally:
                    if found == True:
                        break
                        
            description = driver.find_element(By.CSS_SELECTOR,'[data-qa="vacancy-description"]').get_attribute('outerHTML')
            description = Scrapper.prettify(description)
            print(f'URL: {url}')
            
            db.inputdata(name, salary, company, location, description, url)
                   
        except Exception as ex:
            pass

        finally:
            driver.close()
            driver.quit()
            
    def prettify(smth):
        smth=BeautifulSoup(smth,'lxml').text
        smth=smth.replace("'","")
        return smth
                
    
    def page_count(driver):   
        strategies = [
            (By.CLASS_NAME, "pager"), 
            (By.XPATH, "//nav/ul/li[last()]"),
            (By.XPATH, "//nav/ul/li[last()-1]")
        ]
        found = False
        for strategy in strategies:
            try:
                page_count=driver.find_element(*strategy)

                if strategies.index(strategy)==0: page_count=page_count.find_element(By.XPATH,"span[last()]")

                page_count=page_count.get_attribute('outerHTML')
                page_count=BeautifulSoup(page_count,'lxml').text

                if page_count.startswith('...'): page_count=page_count.split('...')[1]

                page_count=int(page_count)
                
                found = True
            except Exception as ex:
                pass
            finally:
                if found:
                    return(page_count)
                elif strategies.index(strategy)== len(strategies)-1 and not found:
                    return(1)

                    
    def url_list(baseurl,page_count):
        if baseurl.endswith('&page='):
            pass

        elif '&page=' in baseurl:
            parts=baseurl.split('&page=')
            if parts[-1].isdigit():
                baseurl=baseurl[:-1]
                
        else:
            baseurl=baseurl+'&page='

        url_list = []
        for page in range(0,page_count):
            url = baseurl
            url_list.append(f'{url}{page}')
        return(url_list)
