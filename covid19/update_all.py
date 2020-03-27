import scrapy
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
            EstoniaSpider ]

for i in spiders:
    process.crawl( i )
process.start()
