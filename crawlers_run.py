
from ingatlan_com_crawler import IngatlanComCrawler
from mongo_dao import MongoDAO

db_url = 'mongodb://localhost:27017'
db_name = 'house_price_predict'

crawler = IngatlanComCrawler(
              starter_url='https://ingatlan.com/szukites/elado+lakas+baja',
              http_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'})
crawled_data = crawler.crawl()

dao = MongoDAO(conn_url=db_url, dbname=db_name)
dao.insert_documents(crawled_data)

collection_name = dao.collname
print('Visszaolvas db ' + collection_name)
print(len(dao.get_all_documents(collection_name)))
print(dao.get_all_collection_names())