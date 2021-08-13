
from mongo_dao import MongoDAO
import pandas as pd

db_url = 'mongodb://localhost:27017'
db_name = 'house_price_predict'

dao = MongoDAO(conn_url=db_url, dbname=db_name)

all_collections = dict()
all_coll_names = dao.get_all_collection_names()
all_coll_names.sort()

for coll_name in all_coll_names:
    print(coll_name)
    all_collections[coll_name] = pd.DataFrame(dao.get_all_documents(coll_name))
    print(all_collections[coll_name])
    df = all_collections[coll_name]
    if 'price' in df:
        print(df['price'].mean())
        print(df['price'].std())
        print(df['price'].count())
        print(df['price'].min())
        print(df['price'].max())
        print(df[df['price'] < 8000000])