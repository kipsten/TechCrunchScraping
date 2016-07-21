
import scrapy
from techCrunchScraper.items import TechCrunchScraperItem
from bs4 import BeautifulSoup
import re



class TechCrunchScraper(scrapy.Spider):

    startPageNumber = 7780
    endPageNumber = 7790

    #endPageNumber = 3

    name = "TechCrunchScraper"
    allowed_domains = ["techcrunch.com"]
    start_urls = [
        "http://www.techcrunch.com/",
    ]
    
    def parse(self, response):
        if response.status == 404:
            return

        tcArticle = TechCrunchScraperItem()
        
        currentUrl = response.request.url
        currentPageNumber = 1
        IsHomePage = currentUrl.split("/")[-2] == "techcrunch.com"
        if not IsHomePage:
            currentPageNumber = int(currentUrl.split("/")[-2])
            
        for linkItem in response.css('.post-title a'):
            url = linkItem.css('::attr("href")').extract()[0]
            tcArticle["url"] = url
            yield scrapy.Request(url, self.compileArticleInfo)
        

        
        # 7782 is last page on 7/20/2016
        # can be whatever you want
        if currentPageNumber < endPageNumber:
            nextUrl = "http://www.techcrunch.com/page/" + str(currentPageNumber + 1)
            yield scrapy.Request(nextUrl)
    
    
    def compileArticleInfo(self, response):
        tcArticle = TechCrunchScraperItem()
        
        currentUrl = response.request.url
        tcArticle["url"] = currentUrl
        
        tcArticle["title"] = response.css("h1.alpha.tweet-title::text").extract()[0]
        bodyText = ""
         
        soup = BeautifulSoup(response.body, "html.parser")
        
        for p in soup.select(".article-entry > p"):
            addIt = True
            for item in p.find_all(True):
                if item.name != "a":
                    addIt = False
            if addIt:
                bodyText += p.getText()
        newBodyText = bodyText.replace(u"\u00A0", " ").encode("ascii","replace")
        newBodyText = re.sub(r'\\u[0-9a-z]{4}', '*', newBodyText);
        tcArticle["body"] = newBodyText
        
        tcArticle["date"] = response.css(".byline > .timestamp").xpath("@datetime").extract()[0]
        tcArticle["author"] = response.css(".byline > a::text").extract()[0]
        
        #not gonna work, it seems, because the page loads the number of shares dynamically
        '''print "\n\nhow many fb share things, should be one: " + str(len(soup.find_all("div", class_="total-facebook")[0])) + "\n\n" 
        print "\n\n contents is " + str(soup.find_all("div", class_="total-facebook")[0].contents) + "\n\n"
        tcArticle["facebookShares"] = (soup.find_all("div", class_="total-facebook")[0]).get_text()
        tcArticle["twitterShares"] = (soup.find_all("div", class_="total-twitter")[0]).get_text()'''
        
        yield tcArticle
    