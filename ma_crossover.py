import matplotlib.pyplot as plt
from zipline.api import get_open_orders, order_target_percent, record, symbol, schedule_function
from zipline.utils.events import date_rules
 
def initialize(context): 
    context.assets = {
        'a1': symbol('AAPL'), 
        'a2': symbol('GE'),
        'a3': symbol('WMT')
    }
    context.long_period = 30
    context.short_period = 7
    
    schedule_function(ma_crossover, date_rules.every_day())

def ma_crossover(context, data):
    weight = 1.0 / len(context.assets)
    for sym in context.assets.values():
        hist = data.history(sym, 'price', context.long_period, '1d')
        sma_long = hist.mean()
        sma_short = hist[(-1)*context.short_period:].mean()
        open_orders = get_open_orders()
        if sma_long < sma_short:
            if sym not in open_orders:
                order_target_percent(sym, weight)
        elif sma_long > sma_short:
            if sym not in open_orders:
                order_target_percent(sym, -weight)
    
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


