from fastapi import FastAPI, Query
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher

from scrapy_utils.spiders import TheguardianSpider


app = FastAPI(
    title="TL;DR",
	description="Prioritize News Article paragraphs",
	version="0.0.1",
	contact={
		"name":"mahdi khojasteh",
		"email":"s.mahdikhojasteh@gmail.com",
	},
	license_info={
		"name":"MIT",
	},
)


@app.get("/article")
async def get_article(url: str=Query(None, description="url of the news article")):
    url = "https://www.theguardian.com/world/2023/jan/20/chris-hipkins-set-to-become-next-prime-minister-of-new-zealand"
    
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(TheguardianSpider, url=url)
    process.start()

    return results
