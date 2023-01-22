import scrapy


class TheguardianSpider(scrapy.Spider):
    name = 'theguardian_world_news'
    allowed_domains = ['www.theguardian.com']
    # start_urls = ['https://www.theguardian.com/world']

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