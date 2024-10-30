from app.celery import app as celery_app
from app.amazon import AmazonSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.products.models import Brand, Product



@celery_app.task
def run_scrapper():
    start_url = list(Brand.objects.values_list('url', flat=True))
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmazonSpider, start_urls=start_url)
    process.start(install_signal_handlers=False)
    process.stop()

