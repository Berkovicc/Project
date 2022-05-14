#
# This project scrapes stackoverflow for questions tagged with web-scraping and also get related tags from questions to compare number of answers and views 
#
#

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import sys
import time



headers = {
    'accept': 'text/html',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}



if __name__ == "__main__":
    main_url = "https://stackoverflow.com/questions/tagged/"

    # Selenium options for runningg Chrome headless 
    options = Options()
    options.headless = True
    # Windows
    driver = webdriver.Chrome('.\\chromedriver.exe',options=options)

    # we will get more urls from web-scraping page below.
    urls = ["web-scraping"]

    start_time = time.perf_counter()

    driver.get(main_url + urls[0])
    # WebElement
    questions = driver.find_elements_by_xpath("//div[@class='s-post-summary js-post-summary']")
    # To keep track of results
    result_dict = {}
    score_sum = 0
    answer_sum = 0
    view_sum = 0
    
   

    # Get related tag names from questions tagged web-scraping.
    for question in questions:
        # question comes with all text with newline character. Indexes:  0 - votes 2 - answers 4 - views 
        # After 7 comes tags until -3
        info = question.text.split("\n")
        tags = info[8:-3]
        for tag_name in tags:
            if tag_name not in urls:
                urls.append(tag_name)
        score_sum += int(info[0])
        answer_sum += int(info[2])
        view_sum += int(info[4])

    # Let's write results to dictionary and then, pop web-scraping from tags to parse in order to prevent another parse on that tag
    result_dict[urls[0]] = [score_sum,answer_sum,view_sum]
    urls.pop(0)

    score_sum = 0
    answer_sum = 0
    view_sum = 0 


    # Parse all for views and answers
    for url in urls:
        driver.get(main_url + url)  
        questions = driver.find_elements_by_xpath("//div[@class='s-post-summary js-post-summary']")
        for question in questions:
            info = question.text.split("\n")
            score_sum += int(info[0])
            answer_sum += int(info[2])
            view_sum += int(info[4])
        result_dict[url] = [score_sum,answer_sum,view_sum]
        # reset counters
        score_sum = 0
        answer_sum = 0
        view_sum = 0 

    end_time = time.perf_counter()
    # Print result!
    #print(result_dict)
    for key,value in result_dict.items():
        print("============")
        print(key.upper())
        print("Cumulative Score: {}\tCumulative Answers: {}\t Cumulative View: {}".format(value[0],value[1],value[2]))
        print("============")
    print("Performance of this bs4 scraper as seconds is:",end_time - start_time)