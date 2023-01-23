import re
from multiprocessing import Process, Queue
import fastapi
from fastapi import HTTPException, Query

from api.utils.article_services import crawl_and_rank

router = fastapi.APIRouter()


@router.get("/article")
async def get_article(url:str = Query(
                                description="url of the news article", 
                                min_length=5
                            )
):
    supported_urls = [
        "theguardian",
        "bbc",
        "dailymail"
    ]
    pattern = "^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"
    domain = re.search(pattern, url)
    if domain:
        domain_name = domain.group(1).split('.')[0]
        is_supported = [s for s in supported_urls if domain_name in s]
        if not is_supported:
            raise HTTPException(
                status_code=400, detail="url is not supported."
            )
    queue = Queue()  
    p = Process(target=crawl_and_rank, args=(url, domain_name, queue))
    p.start()
    p.join()
    return queue.get()