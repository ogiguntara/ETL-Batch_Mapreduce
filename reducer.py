#!python3

import pandas
import pickle
import json
import time

import connection

from datetime import datetime
from hdfs import InsecureClient

def reduce(shuffled_dict):
    reduced = {}
    
    for i in shuffled_dict: 
        reduced[i] = sum(shuffled_dict[i])
    return reduced


if __name__ == "__main__":
    time = datetime.now().strftime("%Y%m%d")

    file= open('shuffled.pkl','rb')
    shuffled = pickle.load(file)

    conf_hadoop = connection.param_config("hadoop")["ip"]
    client = InsecureClient(conf_hadoop)

    final = reduce(shuffled)
    df = pandas.DataFrame(final, index=[0])
    with client.write(f'/DigitalSkola/{time}/db_mart_quantity_day_{time}.csv', encoding='utf-8') as writer:
            df.to_csv(writer, index=False)

    
    print("Quantity Transaction... ")