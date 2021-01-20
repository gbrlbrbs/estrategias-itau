import matplotlib.pyplot as plt
from zipline.api import get_open_orders, order_target_percent, record, symbol, schedule_function
from zipline.utils.events import date_rules
 
def initialize(context): 
    context.assets = {
        'a1': symbol('AAPL'), 
        'a2': symbol('GE'),
        'a3': symbol('WMT')
    }
    context.has_ordered = False
    
    schedule_function(buy_and_hold, date_rules.every_day())
    

def buy_and_hold(context, data):
    weights = {
        'a1': 0.33,
        'a2': 0.33,
        'a3': 0.33
    }

    if not context.has_ordered:
        for key, sym in context.assets.items():
            open_orders = get_open_orders()
            if sym not in open_orders:
                order_target_percent(sym, weights[key])
        context.has_ordered = True
    
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