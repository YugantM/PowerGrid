import time
import requests
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://localhost:5000/")
driver.refresh()

while True:

    refresh_requried_at = 43
    start = time.time()
    response = requests.get("http://localhost:5000/chart")
    process_time = start -time.time()
    print(response,process_time)
    '''
                if process_time+refresh_requried_at<0:
                    time.sleep(2)
                else:
                    time.sleep(refresh_requried_at+process_time)
                
    '''
    print("reloading..")
    driver.refresh()


