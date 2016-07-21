import scrapy

class TechCrunchScraperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    
    #facebookShares = scrapy.Field()
    #twitterShares = scrapy.Field()
    
    ##desc = scrapy.Field()
    


