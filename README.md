## Crawl cases and save to file
The purpose of this project is to crawl various government websites and collect COVID-19 testing data. This will hopefully aid in quantifying and comparing responses between countries.

## Data
Currently is available for the following countries/states. 

## Spiders
Currently spiders are available for the following countries/states. This is not neccessarily the same the above table because some data is collected manually.

## Dependencies

* [Scrapy](https://scrapy.org/)

## Configuration

1. Add config file (./covid19/config.py) to post ascii tables to URLs (Use case: Slack bot).

```
slack_sandiego_post_url = "<post-url>"
```

2. Create ./logs/ and ./data directories
3. Run command from base directory
```
scrapy crawl --logfile logs/$(date +%Y-%m-%d-%H-%M.log) -o data/items.csv sandiego
```
