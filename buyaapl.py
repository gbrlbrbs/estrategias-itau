import pandas as pd
import matplotlib.pyplot as plt
from zipline.api import order, record, symbol, attach_pipeline
from zipline.pipeline import Pipeline
from zipline.pipeline.factors import SimpleMovingAverage

def initialize(context):
    context.assets = {'AAPL': symbol('AAPL')}


def handle_data(context, data):
    order(context.assets, 1000)
    record(AAPL=data.current(context.asset, 'price'))


def analyze(context=None, results=None):
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('AAPL price (USD)')

    plt.gcf().set_size_inches(18, 8)
    plt.show()


