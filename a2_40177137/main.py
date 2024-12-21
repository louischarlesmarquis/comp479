from scrapy.crawler import CrawlerProcess
from spectrum_spider import SpectrumSpider

def main():
    process = CrawlerProcess()
    process.crawl(SpectrumSpider, file_limit=5) 
    process.start()

if __name__ == "__main__":
    main()
