# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:35:00 2024

@author: Oriana.Rahman
"""

import requests
from time import sleep
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


s = requests.Session()
s.headers.update({'X-API-key': '9V36T36G'}) # Make sure you use YOUR API Key

# global variables
MAX_LONG_EXPOSURE = 300000
MAX_SHORT_EXPOSURE = -100000
ORDER_LIMIT = 5000

def get_tick():
    resp = s.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']


def get_bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        bid_side_book = book['bids']
        ask_side_book = book['asks']
        
        bid_prices_book = [item["price"] for item in bid_side_book]
        ask_prices_book = [item['price'] for item in ask_side_book]
        bid_quantity_book = [item["quantity"] for item in bid_side_book]
        ask_quantity_book = [item["quantity"] for item in ask_side_book]
        bid_id_book = [item["order_id"] for item in bid_side_book] 
        ask_id_book = [item["order_id"] for item in ask_side_book] 
        
        best_bid_price = bid_prices_book[0]
        best_ask_price = ask_prices_book[0]
        
        bid_quantity = bid_quantity_book[0]
        ask_quantity = ask_quantity_book[0]

        bid_id= bid_id_book[0]
        ask_id= ask_id_book[0]

        return best_bid_price, best_ask_price, bid_quantity, ask_quantity, bid_id, ask_id

def get_time_sales(ticker):
    payload = {'ticker': ticker, 'limit': 50}
    resp = s.get ('http://localhost:9999/v1/securities/tas', params = payload)
    if resp.ok:
        book = resp.json()
        time_sales_book = [item["quantity"] for item in book]
        return time_sales_book

def get_time_price(ticker):
    payload = {'ticker': ticker, 'limit': 50}
    resp = s.get ('http://localhost:9999/v1/securities/tas', params = payload)
    if resp.ok:
        book = resp.json()
        time_sales_book = [item["price"] for item in book]
        return time_sales_book


def get_position():
    resp = s.get ('http://localhost:9999/v1/securities')
    if resp.ok:
        book = resp.json()
        return (book[0]['position']) + (book[1]['position']) + (book[2]['position']) + book[3]['position']

def get_open_orders(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/orders', params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders

def get_order_status(order_id):
    resp = s.get ('http://localhost:9999/v1/orders' + '/' + str(order_id))
    if resp.ok:
        order = resp.json()
        return order['status']


def check_first10(array1, array2):
     return np.all(np.array(array1[-250:]) < np.array(array2[-250:]))

def check_first10pos(array1, array2):
     return np.all(np.array(array1[-250:]) > np.array(array2[-250:]))

def main():
    tick, status = get_tick()
    #for i in range(0,96):
    #        s.post('http://localhost:9999/v1/orders', params = {'ticker': 'CROW', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
    #ticker_list = ['OWL','CROW','DOVE','DUCK']
    #s.post('http://localhost:9999/v1/orders', params = {'ticker': 'OWL', 'type': 'MARKET', 'quantity': 5000, 'price': 100, 'action': 'SELL'})
    #s.post('http://localhost:9999/v1/orders', params = {'ticker': 'CROW', 'type': 'MARKET', 'quantity': 5000, 'price': 100, 'action': 'SELL'})
    #s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DOVE', 'type': 'MARKET', 'quantity': 5000, 'price': 100, 'action': 'SELL'})
    #s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DUCK', 'type': 'MARKET', 'quantity': 5000, 'price': 100, 'action': 'BUY'})

    #print(get_time_price("OWL")[0])
    #print(get_position())

    # data = list(reversed(get_time_price("CROW")))# Simulated cumulative sum data

    # df = pd.DataFrame({'Actual': data})

    # # Calculate the moving average
    # sma = list(df['Actual'].rolling(window=10).mean())
    # lma = list(df['Actual'].rolling(window=200).mean())
    # df['S Moving Average'] = df['Actual'].rolling(window=50).mean()
    # df['L Moving Average'] = df['Actual'].rolling(window=200).mean()
    

    # plt.plot(df['Actual'], label='Actual Data', color='blue', alpha=0.7)
    # plt.plot(df['L Moving Average'], label=f'200-point Moving Average', color='red', linewidth=2)
    # plt.plot(df['S Moving Average'], label=f'50-point Moving Average', color='green', linewidth=2)
    # plt.title('Actual Data vs. Moving Average')
    # plt.xlabel('Index')
    # plt.ylabel('Value')
    # plt.legend()
    # plt.grid()
    # plt.show()

    long_positionCrow = 0
    short_positionCrow = 0

    long_positionDove = 0
    short_positionDove = 0

    long_positionDuck = 0
    short_positionDuck = 0

    long_positionOwl = 0
    short_positionOwl = 0

    while status == 'ACTIVE':       

        dataCrow = list(reversed(get_time_price("CROW")))
        dataDuck = list(reversed(get_time_price("DUCK")))
        dataDove = list(reversed(get_time_price("DOVE")))
        dataOwl = list(reversed(get_time_price("OWL")))

        dfCrow = pd.DataFrame({'Actual': dataCrow})
        dfDove = pd.DataFrame({'Actual': dataDove})
        dfDuck = pd.DataFrame({'Actual': dataDuck})
        dfOwl = pd.DataFrame({'Actual': dataOwl})

        smaCrow = list(dfCrow['Actual'].rolling(window=50).mean())
        lmaCrow = list(dfCrow['Actual'].rolling(window=200).mean())

        smaDove = list(dfDove['Actual'].rolling(window=50).mean())
        lmaDove = list(dfDove['Actual'].rolling(window=200).mean())

        smaDuck = list(dfDuck['Actual'].rolling(window=50).mean())
        lmaDuck = list(dfDuck['Actual'].rolling(window=200).mean())

        smaOwl = list(dfOwl['Actual'].rolling(window=50).mean())
        lmaOwl = list(dfOwl['Actual'].rolling(window=200).mean())

 
        if ((short_positionCrow == 0) and (check_first10(smaCrow,lmaCrow))):
            for i in range(0,25):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'CROW', 'type': 'MARKET', 'quantity': 5000,'action': 'SELL'})
            print("CROW SHORT POSITION")
            short_positionCrow = 1
        if (short_positionCrow == 1) and smaCrow[-1] > lmaCrow[-1]:
            for i in range(0,25):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'CROW', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            print("CROW EXIT SHORT POSITION")
            short_positionCrow = 0
        if ((long_positionCrow == 0) and (check_first10pos(smaCrow,lmaCrow))):
            for i in range(0,25):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'CROW', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            long_positionCrow = 1
        if (long_positionCrow == 1) and smaCrow[-1] < lmaCrow[-1]:
            for i in range(0,25):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'CROW', 'type': 'MARKET', 'quantity': 5000,'action': 'SELL'})
            long_positionCrow = 0
    




        if ((short_positionDove == 0) and (check_first10(smaDove,lmaDove))):
            for i in range(0,7):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DOVE', 'type': 'MARKET', 'quantity': 5000, 'action': 'SELL'})
            short_positionDove = 1
        if (short_positionDove == 1) and smaDove[-1] > lmaDove[-1]:
            for i in range(0,7):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DOVE', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            short_positionDove = 0
        if ((long_positionDove == 0) and (check_first10pos(smaDove,lmaDove))):
            for i in range(0,7):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DOVE', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            long_positionDove = 1
        if (long_positionDove == 1) and smaDove[-1] < lmaDove[-1]:
            for i in range(0,7):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DOVE', 'type': 'MARKET', 'quantity': 5000,'action': 'SELL'})
            long_positionDove = 0
        
        

        if ((short_positionDuck == 0) and (check_first10(smaDuck,lmaDuck))):
            for i in range(0,10):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DUCK', 'type': 'MARKET', 'quantity': 5000, 'action': 'SELL'})
            short_positionDuck = 1  
        if (short_positionDuck == 1) and smaDuck[-1] > lmaDuck[-1]:
            for i in range(0,10):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DUCK', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            short_positionDuck = 0
        if ((long_positionDuck == 0) and (check_first10pos(smaDuck,lmaDuck))):
            for i in range(0,10):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DUCK', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            long_positionDuck = 1
        if (long_positionDuck == 1) and smaDuck[-1] < lmaDuck[-1]:
            for i in range(0,10):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'DUCK', 'type': 'MARKET', 'quantity': 5000,'action': 'SELL'})
            long_positionDuck = 0
    

        if ((short_positionOwl == 0) and (check_first10(smaOwl,lmaOwl))):
            for i in range(0,5):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'OWL', 'type': 'MARKET', 'quantity': 5000, 'action': 'SELL'})
            short_positionOwl = 1
        if (short_positionOwl == 1) and smaOwl[-1] > lmaOwl[-1]:
            for i in range(0,5):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'OWL', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            short_positionOwl = 0
        if ((long_positionOwl == 0) and (check_first10pos(smaOwl,lmaOwl))):
            for i in range(0,5):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'OWL', 'type': 'MARKET', 'quantity': 5000,'action': 'BUY'})
            long_positionOwl = 1
        if (long_positionOwl == 1) and smaOwl[-1] < lmaOwl[-1]:
            for i in range(0,5):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': 'OWL', 'type': 'MARKET', 'quantity': 5000,'action': 'SELL'})
            long_positionOwl = 0
 


        tick, status = get_tick()

if __name__ == '__main__':
    main()



