import pandas as pd

from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher

from scrapy_utils.spiders import TheguardianSpider, BBCSpider, DailyMailSpider

from sentence_transformers import SentenceTransformer, util


def crawl_and_rank(url:str, domain_name:str, queue:dict):
    # url = "https://www.theguardian.com/world/2023/jan/20/chris-hipkins-set-to-become-next-prime-minister-of-new-zealand"
    
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    
    if domain_name == "theguardian":
        process.crawl(TheguardianSpider, url=url)
    elif domain_name =="bbc":
        process.crawl(BBCSpider, url=url)
    elif domain_name == "dailymail":
        process.crawl(DailyMailSpider, url=url)
    process.start()

    def get_similarity(model, s1, s2):
        embedding_1= model.encode(s1, convert_to_tensor=True)
        embedding_2 = model.encode(s2, convert_to_tensor=True)

        return util.pytorch_cos_sim(embedding_1, embedding_2).item()
    if results:
        title = results[0]["title"]
        paragraphs = results[0]["paragraphs"]
        df = pd.DataFrame(paragraphs, columns=["paragraph"])
        
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        similarities = df["paragraph"].apply(
            lambda x:get_similarity(model, x, title)
        )

        df['similarity'] = similarities
        df.sort_values('similarity', ascending=False, inplace=True)
        paragraph_numbers = list(map(lambda x:x+1, df.index.to_list()))
        data = {
            "paragraph_numbers": paragraph_numbers,
            "paragraphs": df["paragraph"].to_list(),
            "similarities": df["similarity"].to_list()
        }
        queue.put(data)
    else:
        queue.put(None)
        
