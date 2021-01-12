from operator import ge
import pandas as pd
import matplotlib.pyplot as plt
from zipline.api import get_open_orders, order_target_percent, record, symbol
from zipline.pipeline import Pipeline
from zipline.pipeline.factors import SimpleMovingAverage

def initialize(context):
    context.assets = {
        'AAPL': symbol('AAPL'), 
        'GE': symbol('GE'),
        'WMT': symbol('WMT'),
        'DIS': symbol('DIS'),
        'MSFT': symbol('MSFT'),
        'UAL': symbol('UAL'),
        'GOOGL': symbol('GOOGL'),
        'JPM': symbol('JPM')
    }


def handle_data(context, data):
    percent = 1.0 / len(context.assets)
    for sym in context.assets.values():
        hist = data.history(sym, 'price', 40, '1d')
        sma_21 = hist.mean()
        sma_3 = hist[-10:].mean()

        open_orders = get_open_orders()

        if sma_21 < sma_3:
            if sym not in open_orders:
                order_target_percent(sym, percent)
        elif sma_21 > sma_3:
            if sym not in open_orders:
                order_target_percent(sym, -percent)

        record(leverage = context.account.leverage)


def analyze(context=None, results=None):
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.leverage.plot()
    ax2.set_ylabel('Leverage')

    plt.gcf().set_size_inches(18, 8)
    plt.show()


