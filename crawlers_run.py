
from ingatlan_com_crawler import IngatlanComCrawler
from mongo_dao import MongoDAO
from datetime import date, datetime, timedelta

crawler_url = 'http://ingatlan.com/lista/elado+lakas' # 'http://ingatlan.com/szukites/elado+lakas+baja'
db_url = 'mongodb://localhost:27017'
db_name = 'house_price_predict'
date_format_str = '%d/%m/%Y %H:%M:%S.%f'
page_limit = 30 # feel free to change

crawler = IngatlanComCrawler(
              starter_url=crawler_url,
              http_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'})

last_crawl_date = None
dao = MongoDAO(conn_url=db_url, dbname=db_name)

#while True:
#    if not last_crawl_date or datetime.now() > last_crawl_date + timedelta(minutes=15):
print('Start date: ' + datetime.now().strftime(date_format_str))
last_crawl_date = datetime.now()

# crawl with page limit to reduce memory usage
last_page = crawler.get_last_page_id(crawler_url)
for i in range(last_page//page_limit+1):
        print('CRAWLER get_house_price_predict_data from page {} to {}'.format(str(i*page_limit), str((i+1)*page_limit-1)))
        crawled_data = crawler.crawl(first_page=i*page_limit, last_page=(i+1)*page_limit-1)
        dao.insert_documents(crawled_data)
        del crawled_data

collection_name = dao.collname
print('Visszaolvas db ' + collection_name)
#        print(len(dao.get_all_documents(collection_name)))
print(dao.get_all_collection_names())
print('End date: ' + datetime.now().strftime(date_format_str))
