## Crawl cases and save to file
The purpose of this project is to crawl various government websites and collect COVID-19 testing data. This will hopefully aid in quantifying and comparing responses between countries.

## Data
Currently is available for the following countries/states. 

## Spiders
Currently spiders are available for the following countries/states. This is not neccessarily the same the above table because some data is collected manually.
| Country                     | Region          | Source URL                                                                                                                                     | Notes                                                                                                                                | Additional URL                                                                                                                   | Scrap         |
|-----------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|---------------|
| Bahrain                     | Asia            | [Bahrain Ministry of Health](https://www.moh.gov.bh/COVID19)                                                                                   | Table is in easily accesible format, but translation isn't easy.                                                                     |                                                                                                                                  | Scrapy        |
| Japan                       | Asia            | [covid19japan GitHub](https://github.com/reustle/covid19japan)                                                                                 | Collects data from a number of government sources which I can't read/parse                                                           |                                                                                                                                  | Github        |
| Malaysia                    | Asia            | [Malaysia Ministry of Health](http://www.moh.gov.my/index.php/pages/view/2019-ncov-wuhan)                                                      |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Pakistan                    | Asia            | [Pakistan National Institute of Health](https://www.nih.org.pk/novel-coranavirus-2019-ncov/)                                                   | PDF including testing data from providences is listed here.                                                                          |                                                                                                                                  | Manual        |
| Palestine                   | Asia            | [Corona Virus (COVID-19) in Palestine](http://corona.ps/API/summary)                                                                           | Provide an API for grabbing the current data. Unclear where to get historic data                                                     |                                                                                                                                  | Scrapy        |
| South Korea                 | Asia            | [Coronavirus-Dataset GitHub](https://github.com/jihoo-kim/Coronavirus-Dataset)                                                                 | Had data for tests performed and positive cases up to March 20th. Unclear if still being updated.                                    |                                                                                                                                  | Github        |
| Vietnam                     | Asia            | [Vietnam Ministry of Health](https://ncov.moh.gov.vn/)                                                                                         | Easily parsable table. Also provide testing information at the state-wide level which isn't utilized at the moment.                  |                                                                                                                                  | Scrapy        |
| Costa Rica                  | Central America | [Costa Rica Ministry of Health](https://www.ministeriodesalud.go.cr/index.php/centro-de-prensa/noticias/741-noticias-2020/1532-lineamientos-nacionales-para-la-vigilancia-de-la-infeccion-por-coronavirus-2019-ncov)  |                                                               |                                                                                                                                  | Manual        |
| Austria                     | Europe          | [Austria Ministry of Public Affairs](https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html )  | List number of cases performed and positive cases for the entire country as well as all federal states.                              |                                                                                                                                  | Scrapy        |
| Czech Republic (Czechia)    | Europe          | [Czech Republic Ministry of Health](https://onemocneni-aktualne.mzcr.cz/covid-19)                                                              | Current cases at link which can be scrapped. Past data pulled from wikipedia                                                         | [2020 coronavirus pandemic in the Czech Republic](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Czech_Republic) | Scrapy        |
| Estonia                     | Europe          | [Estonia Government](https://www.kriis.ee/en)                                                                                                  | Tests performed and positive tests provided, but historic data and deaths grabbed manually from interactive application.             | [CoronaCard](https://koroonakaart.ee/en)                                                                                         | Scrapy        |
| Finland                     | Europe          | [Finland Public Health Institute](https://www.fhi.no/sv/smittsomme-sykdommer/corona/)                                                          | Current data is presented on this webpage, historical data is probably available in daily press releases.                            |                                                                                                                                  | Scrapy        |
| Greece                      | Europe          | [2020 coronavirus pandemic in Greece](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Greece)                                       | Information released by greek government in daily PDFs. Will take values from Wikipedia.                                             |                                                                                                                                  | Wikipedia     |
| Hungary                     | Europe          | [Hungary Government](https://koronavirus.gov.hu/)                                                                                              | List total cases and positive cases. Past cases through wayback machine.                                                             |                                                                                                                                  | Scrapy        |
| Iceland                     | Europe          | [Iceland Government](https://www.covid.is/tolulegar-upplysingar)                                                                               | Positive cases can be parsed but total tested in only available in the interactive graphs. Provided a download data option though.   |                                                                                                                                  | Manual        |
| Italy                       | Europe          | [COVID-19 GitHub](https://github.com/pcm-dpc/COVID-19/blob/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv)            | Presidenza del Consiglio dei Ministri is publishing all data on github repository.                                                   |                                                                                                                                  | Github        |
| Latvia                      | Europe          | [Latvia Center for Disease Prevention and Control](https://twitter.com/SPKCentrs/media)                                                        | Official twitter account uploads daily tests results. Haven't found a source for deaths.                                             |                                                                                                                                  | Scrapy        |
| Lithuania                   | Europe          | [Lithuania Ministry of Health](http://sam.lrv.lt/lt/naujienos/koronavirusas)                                                                   | Can parse directly from daily news releases. Historical values were collected from interactive map.                                  |                                                                                                                                  | Scrapy        |
| Poland                      | Europe          | [@micalrg's Google Doc](https://docs.google.com/spreadsheets/d/1ierEhD6gcq51HAm433knjnVwey4ZE5DCnu1bW7PRG3E/edit#gid=1140678265)               | Polish government is tweeting out daily data which is being recorded by @micalrg.                                                    |                                                                                                                                  | Manual        |
| Portugal                    | Europe          | [Portugal Ministry of Health](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/)                                               | Releases number of tests performed and positive tests in interactive table. Can't parse with scrapy but will pull manually.          |                                                                                                                                  | Manual        |
| Romania                     | Europe          | [Romania Ministry of Health](http://www.ms.ro/comunicate/)                                                                                     | Data taken from daily afternoon press briefings. Have to translate so might be errors.                                               |                                                                                                                                  | Manual        |
| United Kingdom              | Europe          | [UK Government](https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public)                                                   | Cummulative test counts are released daily. Data for Northern Ireland and Scotland are also being recorded on @Tomwhite on GitHub    | [covid-19-uk-data GitHub](https://github.com/tomwhite/covid-19-uk-data/tree/master/data)                                         | Scrapy/Github |
| Alberta, Canada             | North America   | [Alberta Provincial Government](https://covid19stats.alberta.ca/)                                                                              | Collated test data can  be found on website provided. Unable to parse, but can be added manually.                                    |                                                                                                                                  | Manual        |
| British Columbia, Canada    | North America   | [British Columbia Center for Disease Control](http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus)            |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Manitoba, Canada            | North America   | [Manitoba Government](https://www.gov.mb.ca/covid19/)                                                                                          |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Canada National Lab         | North America   | [Canada Government](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html)                            | Total number of cases doesn't match negative + positive, so difference is recorded as pending.                                       |                                                                                                                                  | Scrapy        |
| New Brunswick, Canada       | North America   | [New Brunswick Provincial Government](https://www2.gnb.ca/content/gnb/en/departments/ocmoh/cdc/content/respiratory_diseases/coronavirus.html#) |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| NL, Canada                  | North America   | [Newfoundland and Labrador Government](https://www.gov.nl.ca/covid-19/pandemic-update/)                                                        |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Nova Scotia, Canada         | North America   | [Nova Scotia Provincial Government](https://novascotia.ca/coronavirus/)                                                                        |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| NWT, Canada                 | North America   | [Northwest Territories Health and Social Servies](https://www.hss.gov.nt.ca/en/services/coronavirus-disease-covid-19)                          |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Ontario, Canada             | North America   | [Ontario Provincial Government](https://www.ontario.ca/page/2019-novel-coronavirus)                                                            |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Quebec, Canada              | North America   | [Quebec Ministry of Health and Social Services](https://www.msss.gouv.qc.ca/professionnels/maladies-infectieuses/coronavirus-2019-ncov/)       |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| Saskatchewan, Canada        | North America   | [Saskatchewan Government](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan) |                             |                                                                                                                                  | Scrapy        |
| Yukon, Canada               | North America   | [Yukon Government](https://yukon.ca/covid-19)                                                                                                  |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| USA                         | North America   | [Covid Tracking Project](https://covidtracking.com/)                                                                                           | Official sources aren't too good. Will pull from The COVID Tracking Project. Spiders are available for a number of states as backup. |                                                                                                                                  | Github        |
| Australia Capital Territory | Oceania         | [Australia Capital Health Department](https://health.act.gov.au/public-health-alert/updated-information-about-covid-19)                        |                                                                                                                                      |                                                                                                                                  | Scrapy        |
| New South Wales, Australia  | Oceania         | [NSW Health Department](https://www.health.nsw.gov.au/news/Pages/default.aspx)                                                                 | Press briefings are available at the link which are individually grabbed and parse                                                   |                                                                                                                                  | Scrapy        |
| Philippines                 | Oceania         | [Philippines Department of Health](https://www.doh.gov.ph/2019-nCoV/)                                                                          | Can find negative and positve test results, but not deaths. Need additional source besides interactive maps.                         |                                                                                                                                  | Scrapy        |
| --------------------------- | --------------- | ----------------------- | ---------------------------------------------------------------------------------- | -------------------------- | ------------- |

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
