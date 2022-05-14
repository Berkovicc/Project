#
# This project scrapes stackoverflow for questions tagged with web-scraping and also get related tags from questions to compare number of answers and views 
#
#


import requests
import bs4
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

    # we will get more urls from web-scraping page below.
    urls = ["web-scraping"]

    start_time = time.perf_counter()

    response = requests.get(main_url+urls[0],headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    questions = soup.find_all("div",id=re.compile("question-summary-*"))
    # To keep track of results
    result_dict = {}
    score_sum = 0
    answer_sum = 0
    view_sum = 0
    
   

    # Get related tag names from questions tagged web-scraping.
    for question in questions:
        tag_name = question.find_all(rel="tag")[0]["href"].split("/")[-1]
        if tag_name not in urls:
            urls.append(tag_name)
        #  int(a[0].find_all("div",class_="s-post-summary--stats-item")[0].text.split("\n")[1])
        stats = question.find_all("div",class_="s-post-summary--stats-item")
        score_sum += int(stats[0].text.split("\n")[1])
        answer_sum += int(stats[1].text.split("\n")[1])
        view_sum += int(stats[2].text.split("\n")[1])

    # Let's write results to dictionary and then, pop web-scraping from tags to parse in order to prevent another parse on that tag
    result_dict[urls[0]] = [score_sum,answer_sum,view_sum]
    urls.pop(0)

    score_sum = 0
    answer_sum = 0
    view_sum = 0 


    # Parse all for views and answers
    for url in urls:
        response = requests.get(main_url + url,headers=headers)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        # 0 - votes, 1 - answers, 2 - views  
        questions = soup.find_all("div",id=re.compile("question-summary-*"))
        for question in questions:
            stats = question.find_all("div",class_="s-post-summary--stats-item")
            score_sum += int(stats[0].text.split("\n")[1])
            answer_sum += int(stats[1].text.split("\n")[1])
            view_sum += int(stats[2].text.split("\n")[1])
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