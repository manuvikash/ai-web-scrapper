import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time

def scrape(website):
    print("Launching browser")

    driverPath = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option ('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(driverPath), options=options)

    try:
        driver.get(website)
        time.sleep(10)
        print("Page loaded")
        html = driver.page_source

        return html

    finally:
        driver.quit()

# res = scrape("https://www.wearcomet.com/")
# print(res)