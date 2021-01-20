import matplotlib.pyplot as plt
from zipline.api import get_open_orders, order_target_percent, record, symbol, schedule_function
from zipline.utils.events import date_rules
 
def initialize(context): 
    context.assets = {
        'a1': symbol('AAPL'), 
        'a2': symbol('GE'),
        'a3': symbol('WMT')
    }
    context.time_window = 20
    
    schedule_function(volatility_handle, date_rules.every_day())
    

def volatility_handle(context, data):
    # calculate vols and weights 
    volatilities = {}
    
    for key, sym in context.assets.items():
        hist = data.history(sym, 'price', context.time_window, '1d')
        volatilities[key] = hist.std()
    
    weights = {}
    denominator = volatilities['a1']*volatilities['a2'] + volatilities['a2']*volatilities['a3'] + volatilities['a3']*volatilities['a1']

    weights['a1'] = volatilities['a2']*volatilities['a3']/denominator
    weights['a2'] = volatilities['a3']*volatilities['a1']/denominator
    weights['a3'] = volatilities['a1']*volatilities['a2']/denominator

    # order
    for key, sym in context.assets.items():
        open_orders = get_open_orders()
        if sym not in open_orders:
            order_target_percent(sym, weights[key])
        
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