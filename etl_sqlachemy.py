# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 02:12:45 2018

@author: rodri
"""
  
# handler.py
#import pymysql
import boto3
import datetime
import json
import logging
import os
import pprint
from datetime import date
from base64 import b64decode

import requests
from sqlalchemy import create_engine, MetaData, text, Table, Column, Integer, String, DateTime, Boolean, Numeric

SAMPLE_ENDPOINT = "https://api.coinmarketcap.com/v1/ticker"

#Encrypt connection string
DB_CONN=os.environ.get('DB_CONN')
#Decrypt
DB_CONN=boto3.client('kms').decrypt(CiphertextBlob=b64decode(DB_CONN))['Plaintext'].decode('utf-8')

# coins numbers get from API
NUM_COINS=os.environ.get('NUM_COINS')

#### Raw API calls
def get_data(limit):
    payload = {
      'limit': limit
    }

    resp = requests.get(SAMPLE_ENDPOINT, params=payload)
    resp.raise_for_status()
    data = resp.json()

    return data

def cleanup(item):
    return {
        "name": item.get("name", ''),
        "symbol": item.get("symbol", ''),
        "rank": int(item.get("rank", 0)),
        "price_usd": float(item.get("price_usd", 0.0)),
        "24h_volume_usd": float(item.get("24h_volume_usd", 0.0)),
        "total_supply": float(item.get("total_supply", 0.0)),
        "percent_change_1h": float(item.get("percent_change_1h", 0.0)),
        "last_updated": make_datetime(int(item.get("last_updated", 0))),
    }

#### util methods
def make_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


# SQL Tables
metadata = MetaData()

sample_table = Table('sample_coinmarketcap', metadata,
    Column('name', String(100), nullable=True),
    Column('symbol', String(100), nullable=True),
    Column('rank', Integer, nullable=True),
    Column('price_usd', Numeric, nullable=True),
    Column('24h_volume_usd', Numeric, nullable=True),
    Column('total_supply', Numeric, nullable=True),
    Column('percent_change_1h', Numeric, nullable=True),
    Column('last_updated', DateTime, nullable=False)
)

def init_tables(engine):
    #sample_table.drop(engine, checkfirst=True)
    metadata.create_all(engine)

def main(event, context):

    # get sample data
    data = get_data(NUM_COINS)

    sample_data = [cleanup(item)
                    for item in data]

    engine = create_engine(DB_CONN)
    init_tables(engine)
    conn = engine.connect()

    conn.execute(sample_table.insert().values(sample_data))

    #pprint.pprint(sample_data)
    
    return "Execution OK!"


if __name__ == "__main__":
    main(None, None)