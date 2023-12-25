
from threading import Thread

from API import API_KEY, API_SEKRET
from binance.client import Client



client = Client(API_KEY, API_SEKRET)


#================================
symbol = '1000PEPEUSDT'
quantity_dollars = 30
round_price = 7

#================================


def price_symbol(symbol):
    price_symbol = client.futures_mark_price(symbol=symbol)
    price_symbol = float(price_symbol['markPrice'])
    print('Ціна: ', price_symbol)
    return price_symbol

#Останній лімітний ордер
def last_limit_order(symbol):
    trades = client.futures_account_trades(symbol=symbol)
    last_trade = float(trades[-1]['price'])
    print(last_trade)
    return last_trade


# Обчислення загального балансу в позиції
def balans_open_positions(symbol):
    open_positions = client.futures_position_information(symbol=symbol)
    for position in open_positions:
        balans_open = float(position['positionAmt'])
    balans_open = round(balans_open * price_symbol(symbol), 1)
    print('Баланс в позиції: ',balans_open)
    return balans_open


#Визначання збитку в позиції
def position_on(symbol):
    positions = client.futures_position_information(symbol=symbol)
    position = positions[0]
    entry_price = float(position['entryPrice'])
    mark_price = float(position['markPrice'])
    quantity = float(position['positionAmt'])
    profit = round((mark_price - entry_price) * quantity, round_price)
    print('Прибуток/Збиток в позиції: ', profit)
    return profit


#=======================================================
# Визначаємо кількість у позиції long
def quantity_long(quantity_dollars):
    # balans = balans_open_positions(symbol)
    last_order_long = last_limit_order(symbol)
    quantity_dollars_long = round(quantity_dollars/last_order_long)

    # if balans > quantity_dollars*2.1:
    #     quantity_long = round(10/last_order_long)
    # elif balans > quantity_dollars*1.1:
    #     quantity_long = round((quantity_dollars*0.6)/last_order_long)
    # else:
    #     quantity_long = quantity_t
    print('Кількість знизу: ',quantity_dollars_long)
    return quantity_dollars_long

def quantity_short(quantity_dollars):
    # balans = balans_open_positions(symbol)
    last_order_short = last_limit_order(symbol)
    quantity_dollars_short = round(quantity_dollars/last_order_short)

    # if balans > quantity_dollars*2.1:
    #     quantity_long = round(10/last_order_long)
    # elif balans > quantity_dollars*1.1:
    #     quantity_long = round((quantity_dollars*0.6)/last_order_long)
    # else:
    #     quantity_long = quantity_t
    print('Кількість short: ',quantity_dollars_short)
    return quantity_dollars_short


#============================================================
# Визначаємо де будуть стояти лімітки long
def limit_order_long_1():
    last_limit_order_min = last_limit_order(symbol)

    limit_order_long1 = round(last_limit_order_min - (last_limit_order_min*0.03), round_price)
    print('Лімітка знизу: ',limit_order_long1)
    return limit_order_long1

def limit_order_long_2():
    last_limit_order_min = last_limit_order(symbol)

    limit_order_long1 = round(last_limit_order_min - (last_limit_order_min*0.06), round_price)
    print('Лімітка знизу: ',limit_order_long1)
    return limit_order_long1

def limit_order_short_1():
    last_limit_order_min = last_limit_order(symbol)

    limit_order_short1 = round(last_limit_order_min + (last_limit_order_min*0.03), round_price)
    print('Лімітка знизу: ',limit_order_short1)
    return limit_order_short1

def limit_order_short_2():
    last_limit_order_min = last_limit_order(symbol)

    limit_order_short1 = round(last_limit_order_min + (last_limit_order_min*0.06), round_price)
    print('Лімітка знизу: ',limit_order_short1)
    return limit_order_short1


#=========================================================
def on_position_long(symbol):
    position_long = client.futures_get_open_orders(symbol=symbol)
    a = 0
    for position in position_long:
        position_side = position['side']
        if position_side == 'BUY':
            a += 1
    print('Поставлено ліміток: ', a)
    return a

def on_position_short(symbol):
    position_short = client.futures_get_open_orders(symbol=symbol)
    a = 0
    for position in position_short:
        position_side = position['side']
        if position_side == 'SELL':
            a += 1
    print('Поставлено ліміток: ', a)
    return a


#====================================================
def create_order_long_1():
    client.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    quantity=quantity_long(quantity_dollars),
                    price=limit_order_long_1(),
                    timeInForce='GTC'
                )

def create_order_long_2():
    client.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    quantity=quantity_long(quantity_dollars),
                    price=limit_order_long_2(),
                    timeInForce='GTC'
                )

def create_order_short_1():
    client.futures_create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity= quantity_short(quantity_dollars),
                        price= limit_order_short_1(),
                        timeInForce='GTC'
                    )

def create_order_short_2():
    client.futures_create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity= quantity_short(quantity_dollars),
                        price= limit_order_short_2(),
                        timeInForce='GTC'
                    )



def work_long():
    while True:
        on_position_long1 = on_position_long(symbol)
        if 1 <= on_position_long1 < 2:
            create_order_long_2()
        elif on_position_long1 < 1:
                create_order_long_1()



def work_short():
    while True:
        on_position_short1 = on_position_short(symbol)
        if 1 <= on_position_short1 < 2:
            create_order_short_2()
        elif on_position_short1 < 1:
                create_order_short_1()



if __name__ == "__main__":
    Thread(target=work_long).start()
    Thread(target=work_short).start()