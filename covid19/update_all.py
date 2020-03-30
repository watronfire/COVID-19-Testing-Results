import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from covid19.spiders.international.australiacapital import AustraliaSpider
from covid19.spiders.international.australiansw import AustraliaNSWSpider
from covid19.spiders.international.austria import AustriaSpider
from covid19.spiders.international.bahrain import BahrainSpider
from covid19.spiders.international.canadaalberta import CanadaAlbertaSpider
from covid19.spiders.international.canadabritishcolumbia import CanadaBritishColumbiaSpider
from covid19.spiders.international.canadanational import CanadaNationalSpider
from covid19.spiders.international.canadanb import CanadaNewBrunswickSpider
from covid19.spiders.international.canadanovascotia import CanadaNovaScotiaSpider
from covid19.spiders.international.canadaontario import CanadaOntarioSpider
from covid19.spiders.international.canadaquebec import CanadaQuebecSpider
from covid19.spiders.international.czechrebublic import CzechRebublicSpider
from covid19.spiders.international.estonia import EstoniaSpider
from covid19.spiders.international.hungary import HungarySpider
from covid19.spiders.international.lithuania import LithuaniaSpider
from covid19.spiders.international.malaysia import MalaysiaSpider
from covid19.spiders.international.norway import NorwaySpider
from covid19.spiders.international.unitedkingdom import UKSpider
from covid19.spiders.international.vietnam import VietnamSpider

process = CrawlerProcess( get_project_settings() )
spiders = [ AustraliaSpider,
            AustraliaNSWSpider,
            AustriaSpider,
            BahrainSpider,
            CanadaAlbertaSpider,
            CanadaOntarioSpider,
            CanadaBritishColumbiaSpider,
            CanadaNationalSpider,
            CanadaNewBrunswickSpider,
            CanadaNovaScotiaSpider,
            CanadaQuebecSpider,
            CzechRebublicSpider,
            HungarySpider,
            UKSpider,
            VietnamSpider,
            LithuaniaSpider,
            MalaysiaSpider,
            EstoniaSpider,
            NorwaySpider ]

for i in spiders:
    process.crawl( i )
process.start()

daily = pd.read_csv( "/Users/natem/Dropbox (Scripps Research)/Personal/Code/Python/crawl-covid19-cases/data/cleaned_international.csv" )
daily["date"] = pd.to_datetime( daily["date"] )

dates = pd.date_range( pd.to_datetime( "2020-02-20" ), daily["date"].max() )
locations = pd.unique( daily["name"] )
completeness = pd.DataFrame( np.zeros( (len(dates), len(locations) ) ) )
completeness.columns = locations
completeness.index = dates

for i in daily.loc[daily["date"] >= pd.to_datetime( "2020-02-20" )].iterrows():
    completeness.loc[i[1]["date"], i[1]["name"]] += 1
completeness.index = completeness.index.date

plt.figure( dpi=100, figsize=(10,10) )
sns.heatmap( completeness, vmin=0 )
plt.savefig( '/Users/natem/Dropbox (Scripps Research)/Personal/Code/Python/crawl-covid19-cases/images/completeness.png' )