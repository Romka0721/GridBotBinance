from binance.client import Client
from API import API_KEY, API_SEKRET

client = Client(API_KEY, API_SEKRET)


SYMBOL = 'SUIUSDT'
QU_DOLLARS = 30


class SymbolInfo:
    def __init__(self, symbol):
        self.symbol = symbol

    def last_open_limit_order(self):
        trades = client.futures_account_trades(symbol=self.symbol)
        last_trade = float(trades[-1]['price'])
        return last_trade

    def balance_on_position(self):
        positions = client.futures_position_information(symbol=self.symbol)
        position = positions[0]
        return float(position['notional']), float(position['unRealizedProfit'])

    def open_quantity_position(self):
        return len(client.futures_get_open_orders(symbol=self.symbol))


class LimitOrderPosition:
    def __init__(self, symbol, dollars):
        self.symbol = symbol
        self.dollars = dollars

    def limit_order_long(self):
        balance_on_position = SymbolInfo.balance_on_position(self.symbol)

        print(balance_on_position)


class CreateOrder:
    def __init__(self, symbol, quantity, price):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

    def create_order_long(self):
        create_order = client.futures_create_order(
            symbol=self.symbol,
            side='BUY',
            type='LIMIT',
            quantity=self.quantity,
            price=self.price,
            timeInForce='GTC'
        )
        return create_order

    def create_order_short(self):
        create_order = client.futures_create_order(
            symbol=self.symbol,
            side='SELL',
            type='LIMIT',
            quantity=self.quantity,
            price=self.price,
            timeInForce='GTC'
        )
        return create_order

    def create_order_close_position(self):
        client.futures_cancel_all_open_orders(symbol=self.symbol)
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
            return create_order


def main():
    while True:
        pass


if __name__ == "__main__":
    trade_work = SymbolInfo(SYMBOL)
    trade_work_position = LimitOrderPosition(SYMBOL, QU_DOLLARS)
