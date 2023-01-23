
# Ranking Article Paragraphs

a webapi which extracts the most important paragraph of a given multi-paragraph text, using transformers library, scrapy and fastapi


## API Reference

#### scrape the article of the given url and rank the paragraphs

```http
  GET /article
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` (query) | `string` | **Required**. url of the article |

### supported news articles for scraping:
- theguardian
- bbc
- dailymail


