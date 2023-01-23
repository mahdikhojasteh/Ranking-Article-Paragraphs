import scrapy


class TheguardianSpider(scrapy.Spider):
    name = 'theguardian_world_news'
    allowed_domains = ['www.theguardian.com']

    def __init__(self, url):
        self.start_urls = [url]

    def parse(self, response):
        title = response.xpath('//main/descendant::h1/text()').get()
        paragraphs = response.xpath('//*[@id="maincontent"]/div/p')
        paragraph_list = []
        for paragraph in paragraphs:
            paragraph_list.append("".join(paragraph.xpath(".//descendant-or-self::*/text()").getall()))
            
        yield {
            "title":title,
            "paragraphs":paragraph_list,
        }

class BBCSpider(scrapy.Spider):
    name = 'bbc_news'
    allowed_domains = ['www.bbc.com']

    def __init__(self, url):
        self.start_urls = [url]

    def parse(self, response):
        title = response.xpath('//*[@id="main-heading"]/text()').get()
        paragraphs = response.xpath('//article/div[@data-component="text-block"]/div/p')
        paragraph_list = []
        for paragraph in paragraphs:
            paragraph_list.append("".join(paragraph.xpath(".//descendant-or-self::*/text()").getall()))
            
        yield {
            "title":title,
            "paragraphs":paragraph_list,
        }


class DailyMailSpider(scrapy.Spider):
    name = 'daily_mail_news'
    allowed_domains = ['www.theguardian.com']

    def __init__(self, url):
        self.start_urls = [url]

    def parse(self, response):
        title = response.xpath('//*[@id="js-article-text"]/h2/text()').get()
        paragraphs = response.xpath('//*[@id="js-article-text"]/div/p')
        paragraph_list = []
        for paragraph in paragraphs:
            paragraph_list.append("".join(paragraph.xpath(".//descendant-or-self::*/text()").getall()))
            
        yield {
            "title":title,
            "paragraphs":paragraph_list,
        }