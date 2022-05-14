import scrapy
import re
import sys


headers = {
    'accept': 'text/html',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}


class StackSpider(scrapy.Spider):
    name = "stackoverflowspider"
    main_url = "https://stackoverflow.com/questions/tagged/"
    # To have a phases to scrape
    initial = True
    
    # we will get more urls from web-scraping page below.
    urls = ["web-scraping"]
    start_urls = [main_url+urls[0]]
    score_sum = 0
    answer_sum = 0
    view_sum = 0
    result_dict = {}

    def yield_tag(self):
        if self.urls:
            url = self.urls.pop(0)
            print("Scraping tag ",url)
            return scrapy.Request(self.main_url+url,callback=self.parse)
        else:
            print("All tags are done! Check Scrapy stats from screen for performance metrics!")

    def parse(self,response):
        # web-scraping tag scraping phase
        if self.initial:
            questions = response.xpath("//div[@class='s-post-summary js-post-summary']")
            tags =questions.xpath("//a[@rel='tag']/text()").getall()
            stats = questions.xpath('//span[@class="s-post-summary--stats-item-number"]/text()').extract()
            for tag_name in tags:
                if tag_name not in self.urls:
                    self.urls.append(tag_name)
                    #self.start_urls.append(self.main_url+tag_name)
            for i in range(0,len(stats),3):
                self.score_sum += int(stats[i])
                self.answer_sum += int(stats[i+1])
                self.view_sum += int(stats[i+2])
            self.initial = False
            # can be used for further processing
            self.result_dict[self.urls[0]] = [self.score_sum,self.answer_sum,self.view_sum]
            self.urls.pop(0)
            #self.start_urls.pop(0)
            print("============")
            print(response.request.url.split("/")[-1].upper())
            print("Cumulative Score: {}\tCumulative Answers: {}\t Cumulative View: {}".format(self.score_sum,self.answer_sum,self.view_sum))
            print("============")
            # reset counters
            self.score_sum = 0
            self.answer_sum = 0
            self.view_sum = 0
            yield self.yield_tag()
        else:
            # for some reason, some tags seems to have different structure
            try:
                questions = response.xpath("//div[@class='s-post-summary js-post-summary']")
                stats = questions.xpath('//span[@class="s-post-summary--stats-item-number"]/text()').extract()
                for i in range(0,len(stats),3):
                    self.score_sum += int(stats[i])
                    self.answer_sum += int(stats[i+1])
                    self.view_sum += int(stats[i+2])
                # can be used for further processing
                self.result_dict[response.request.url] = [self.score_sum,self.answer_sum,self.view_sum]
                print("============")
                print(response.request.url.split("/")[-1].upper())
                print("Cumulative Score: {}\tCumulative Answers: {}\t Cumulative View: {}".format(self.score_sum,self.answer_sum,self.view_sum))
                print("============")
                 # reset counter
                self.score_sum = 0
                self.answer_sum = 0
                self.view_sum = 0
                yield self.yield_tag()
            except:
                yield self.yield_tag()