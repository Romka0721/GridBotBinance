

from binance.client import Client
from API import API_KEY, API_SEKRET
from bot import send_message

client = Client(API_KEY, API_SEKRET)


class SymbolInfo:
    def __init__(self, symbol):
        self.symbol = symbol

    def last_open_limit_order(self):
        trades = client.futures_account_trades(symbol=self.symbol)
        last_trade = float(trades[-1]['price'])
        print(f'Останній закритий лімітний ордер: {last_trade}')
        return last_trade

    def balance_on_position(self):
        positions = client.futures_position_information(symbol=self.symbol)
        position = positions[0]
        a = float(position['notional']), float(position['unRealizedProfit'])
        print(f'Баланс в позиції: {a}')
        return a

    def open_quantity_position(self):
        a = len(client.futures_get_open_orders(symbol=self.symbol))
        print(f'Кількість ліміток: {a}')
        return a


class LimitOrderPosition:
    def __init__(self, symbol, dollars):
        self.symbol = symbol
        self.dollars = dollars
        self.last_limit_order = SymbolInfo(self.symbol).last_open_limit_order()
        self.balance_on_position = SymbolInfo(self.symbol).balance_on_position()[0]
        self.quantity_coin = round(self.dollars / self.last_limit_order, 2)
        if self.symbol == '1000PEPEUSDT':
            self.round_tiker = 7
        else:
            self.round_tiker = 4

    def limit_order_long(self):
        if self.balance_on_position < self.dollars * -5 or self.balance_on_position > self.dollars * 3:
            limit_order_long = round(self.last_limit_order - (self.last_limit_order * 0.06), self.round_tiker)
        elif self.balance_on_position < self.dollars * -3 or self.balance_on_position > self.dollars * 2:
            limit_order_long = round(self.last_limit_order - (self.last_limit_order * 0.045), self.round_tiker)
        else:
            limit_order_long = round(self.last_limit_order - (self.last_limit_order * 0.03), self.round_tiker)
        print(f'Лімітний ордер лонг: {limit_order_long}')
        return limit_order_long

    def limit_order_short(self):
        if self.balance_on_position < self.dollars * -3 or self.balance_on_position > self.dollars * 5:
            limit_order_short = round(self.last_limit_order + (self.last_limit_order * 0.06), self.round_tiker)
        elif self.balance_on_position < self.dollars * -2 or self.balance_on_position > self.dollars * 3:
            limit_order_short = round(self.last_limit_order + (self.last_limit_order * 0.045), self.round_tiker)
        else:
            limit_order_short = round(self.last_limit_order + (self.last_limit_order * 0.03), self.round_tiker)
        print(f'Лімітний ордер шорт: {limit_order_short}')
        return limit_order_short

    def quantity_order_long(self):
        if self.balance_on_position > self.dollars * 3:
            quantity_order_long = round(10 / self.last_limit_order)
        elif self.balance_on_position > self.dollars * 1.6:
            quantity_order_long = round((self.dollars * 0.6) / self.last_limit_order)
        else:
            quantity_order_long = round(self.quantity_coin)
        print(f'Кількість в позиції в лонг: {quantity_order_long}')
        return quantity_order_long

    def quantity_order_short(self):
        if self.balance_on_position < self.dollars * -3:
            quantity_order_short = round(10 / self.last_limit_order)
        elif self.balance_on_position < self.dollars * -1.6:
            quantity_order_short = round((self.dollars * 0.6) / self.last_limit_order)
        else:
            quantity_order_short = round(self.quantity_coin)
        print(f'Кількість в позиції в шорт: {quantity_order_short}')
        return quantity_order_short


class CreateOrder:
    def __init__(self, symbol):
        self.symbol = symbol

    def create_order_long(self, quantity, price):
        create_order = client.futures_create_order(
            symbol=self.symbol,
            side='BUY',
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        result = (f"{self.symbol}: order long.\n"
                  f"Price: {float(create_order['price'])}\n"
                  f"Quantity: {round(float(create_order['origQty']), 2)}")
        print(f'Ордер лонг: {create_order}')
        send_message(result)
        return create_order

    def create_order_short(self, quantity, price):
        create_order = client.futures_create_order(
            symbol=self.symbol,
            side='SELL',
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        result = (f"{self.symbol}: order short.\n"
                  f"Price: {float(create_order['price'])}\n"
                  f"Quantity: {round(float(create_order['origQty']), 2)}")
        print(f'Ордер шорт: {create_order}')
        send_message(result)
        return create_order

    def delete_orders(self):
        client.futures_cancel_all_open_orders(symbol=self.symbol)
        print(f'Закрив всі ордери')

    def close_position(self):
        open_positions = client.futures_position_information(symbol=self.symbol)
        for position in open_positions:
            if float(position['positionAmt']) > 0:
                side = 'SELL'
            else:
                side = 'BUY'
            quantity = abs(float(position['positionAmt']))
            create_order = client.futures_create_order(
                symbol=self.symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            print(f'Закрив всю позицію: {create_order}')
            return create_order
