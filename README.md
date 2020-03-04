## Crawl cases and save to file

## Dependencies

* [Scrapy](https://scrapy.org/)

## Configuration

1. Add Config file (./covid19/config.py) to post ascii tables to URLs (Use case: Slack bot).

```
slack_sandiego_post_url = "<post-url>"
```

2. Create ./logs/ and ./data directories
3. Run command from base directory
```
scrapy crawl --logfile logs/$(date +%Y-%m-%d-%H-%M.log) -o data/items.csv sandiego
```
