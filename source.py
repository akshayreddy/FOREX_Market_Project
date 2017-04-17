
from time import sleep
import time
from ib.ext.Contract import Contract
from ib.opt import Connection, message
import matplotlib
import numpy
from pandas import *
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd

data={'time_stamp':[],'bid_size':[],'ask_size':[],'bid_price':[],'ask_price':[],'last_price':[],'high_price':[],'low_price':[],'close_price':[]}
Type=['time_stamp','bid_size','ask_size','bid_price','ask_price','last_price','high_price','low_price','close_price']

def make_contract(symbol, sec_type, exch, curr):

    Contract.m_symbol = symbol
    Contract.m_secType = sec_type
    Contract.m_exchange = exch
    Contract.m_currency = curr
    return Contract

def watcher(msg):
    print msg

def my_BidAsk(msg):

    TickPrice={'time_stamp':0,'bid_size':0,'ask_size':0,'bid_price':0,'ask_price':0,'last_price':0,'high_price':0,'low_price':0,'close_price':0}

    TickPrice['time_stamp'] = time.time()

    if msg.field == 1:
        TickPrice['bid_price']=msg.price
    elif msg.field == 2:
        TickPrice['ask_price']=msg.price
    elif msg.field == 0:
        TickPrice['ask_size']=msg.size
    elif msg.field == 3:
        TickPrice['bid_size']=msg.size
    elif msg.field == 4:
        TickPrice['last_price']=msg.price
    elif msg.field == 6:
        TickPrice['high_price']=msg.price
    elif msg.field == 7:
        TickPrice['low_price']=msg.price
    elif msg.field == 7:
        TickPrice['close_price']=msg.price

    for type in TickPrice:
        data[type].append(TickPrice[type])


def main():
    conn = Connection.create(port=7497, clientId=999)
    conn.registerAll(watcher)
    showBidAskOnly = True
    if showBidAskOnly:
        conn.unregister(watcher, message.tickSize, message.tickPrice,
                       message.tickString, message.tickOptionComputation)
        conn.register(my_BidAsk, message.tickPrice,message.tickSize)
    conn.connect()
    sleep(1)

    tickId=25861
    cont = make_contract('EUR', 'CASH', 'IDEALPRO', 'USD')

    print '* * * * REQUESTING MARKET DATA * * * *'
    conn.reqMktData(tickId, cont, '', False)
    sleep(60)                                                  #time window of 60 seconds
    print '* * * * CANCELING MARKET DATA * * * *'
    conn.cancelMktData(tickId)


    sleep(1)
    conn.disconnect()
    sleep(1)


main()

#print data
df=pd.DataFrame(data)
df.set_index('time_stamp', inplace=True)
df.to_html("streamed_data.html")                 # Displaying the streamed data on to a html file
df.to_csv('streamed_data.csv')                   # Storing the data in csv file (will not be used)

df=df.cumsum()

#df.plot()                                        # To plot all the fields

df[['bid_size','ask_size','bid_price','ask_price']].plot(title="Plot 1")
#df[['bid_price','ask_price']].plot(title="Plot 2")

plt.show()
