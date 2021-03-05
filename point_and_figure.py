import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PNF:
    def __init__(self, data, box_size, reversal):
        self.box_size = box_size
        self.reversal = reversal
        self.data = data
        self.pnf = []
        self.min = 0
        self.max = 0
        self.construct()

    def construct(self):
        current_trend = []
        trend_min = 0
        trend_max = 0
        trend_symbol = 'X'
        for row in self.data:
            high = row['High']
            low = row['Low']
            close = row['Close']
            point = {}
            rounded_price = self.decimal_round(close if trend_symbol == 'X' else close, self.box_size)
            point['price'] = rounded_price
            if not current_trend:
                print(f"UPTREND STARTED AT {rounded_price}")
                point['dir'] = trend_symbol
                trend_min = trend_max = self.min = self.max = rounded_price
                current_trend.append(point)
                continue

            self.min = min(self.min, rounded_price)
            self.max = max(self.max, rounded_price)
            # up trend reversed
            if trend_symbol == 'X' and rounded_price <= trend_max - (self.reversal * self.box_size):
                print(f"UPTREND REVERSED AT {rounded_price}")
                point['dir'] = trend_symbol = 'O'
                self.pnf.append(current_trend)
                current_trend = []
                trend_min = rounded_price
                trend_max = trend_max - self.box_size
                self.add_to_trend(point, current_trend, trend_min, trend_max)
            elif trend_symbol == 'X' and rounded_price > trend_max - (self.reversal * self.box_size):
                point['dir'] = 'X'
                self.add_to_trend(point, current_trend, trend_min, trend_max)
                trend_min = min(trend_min, rounded_price)
                trend_max = max(trend_max, rounded_price)
            elif trend_symbol == 'O' and rounded_price >= trend_min + (self.reversal * self.box_size):
                print(f"DOWNTREND REVERSED AT {rounded_price}")
                point['dir'] = trend_symbol = 'X'
                self.pnf.append(current_trend)
                current_trend = []
                trend_min = trend_min + self.box_size
                trend_max = rounded_price
                self.add_to_trend(point, current_trend, trend_min, trend_max)
            else:
                point['dir'] = 'O'
                self.add_to_trend(point, current_trend, trend_min, trend_max)
                trend_min = min(trend_min, rounded_price)
                trend_max = max(trend_max, rounded_price)
        
        self.pnf.append(current_trend)

    def add_to_trend(self, point, trend, trend_min, trend_max):
        price = point['price']
        print(f"PRICE: {price}, TRENDMAX: {trend_max}, TRENDMIN: {trend_min}")
        if not trend and price == trend_min:
            for i in np.linspace(trend_max, price, int((trend_max - price + self.box_size)/self.box_size)):
                self._add_to_trend(i, 'O', trend)
        elif not trend and price == trend_max:
            for i in np.linspace(trend_min, price, int((price - trend_min + self.box_size)/self.box_size)):
                self._add_to_trend(i, 'X', trend)
        elif price < trend_min:
            for i in np.linspace(trend_min - self.box_size, price, int((trend_min - price)/self.box_size)):
                self._add_to_trend(i, point['dir'], trend)
        elif price > trend_max:
            for i in np.linspace(trend_max + self.box_size, price, int((price - trend_max)/self.box_size)):
                self._add_to_trend(i, point['dir'], trend)

    def _add_to_trend(self, price, symbol, trend):
        if not any(d['price'] == price for d in trend):
            point = {}
            point['dir'] = symbol
            point['price'] = price
            trend.append(point)

    @staticmethod
    def decimal_round(price, box_size):
        return round(box_size * round(float(price)/box_size), 2)

    def plot(self):
        start = self.min
        box = self.box_size
        changes = [len(a) if a[0]['dir'] == 'X' else -1 * len(a) for a in self.pnf]
        print(changes)
        fig = plt.figure(figsize=(5, 10))
        ax = fig.add_axes([.25, .25, .7, .7])
        pointChanges = []
        for chg in changes:
            pointChanges += [self.sign(chg)] * abs(chg)

        symbol = {-1:'o', 1:'x'}
        color = {-1:'red', 1:'green'}
        for ichg, chg in enumerate(changes):
            x = [ichg+1] * abs(chg)
            y = [start + i * box * self.sign(chg) for i in range(abs(chg))] 
            start += box * self.sign(chg) * (abs(chg)-2)
            ax.scatter(x, y, c=color[self.sign(chg)], marker=symbol[self.sign(chg)], s=175)   #<----- control size of scatter symbol

        ax.set_xlim(0, len(changes)+1)
        fig.savefig('pointandfigure.png')
        plt.show()

    @staticmethod
    def sign(val):
        return val / abs(val)
