from binance.client import Client
import pandas
import time

api_key = 'oRItaq3XZvbaPoUtsJhWMUKqANQCrBj6J2ZWZe33uSTjHOwi1jBzBEg87i4vM3CQ'
api_sekret = 'MHkuhNjS1101IvT3MYor41LehLIk93INL7hunFUUPM5VNUahn0A0jBtNkFX7ziYN'

client = Client(api_key, api_sekret)



tiker = 'SUIUSDT'
quantity_dollars = 50
round_tiker = 4



# Дістаємо ціну
def price_now():
    price_tiker = client.futures_mark_price(symbol=tiker)
    price_tiker = float(price_tiker['markPrice'])
    print('Ціна: ',price_tiker)
    return price_tiker


def last_limit_order():
    trades = client.futures_account_trades(symbol=tiker)
    last_trade = float(trades[-1]['price'])
    print(last_trade)
    return last_trade


price_test = price_now()


# Обчислення загального балансу в позиції
def balans():
    open_positions = client.futures_position_information(symbol=tiker)
    for position in open_positions:
        bal1 = float(position['positionAmt'])
    bal1 = round(bal1*price_test, 1)
    print('Баланс в позиції: ',bal1)
    return bal1


#Визначання збитку в позиції
def position_on():
    positions = client.futures_position_information(symbol=tiker)
    for position in positions:
        if position['symbol'] == tiker:
            entry_price = float(position['entryPrice'])
            mark_price = float(position['markPrice'])
            quantity = float(position['positionAmt'])
            profit = round((mark_price - entry_price) * quantity, 4)
            print('Прибуток/Збиток в позиції: ', profit)
    return profit


# Визначаємо де будуть стояти лімітки
def limit_order_max():
    bal_test = balans()
    if bal_test < quantity_dollars*-3 or bal_test > quantity_dollars*5:
        elem_max = round(price_test + (price_test*0.06), round_tiker)
    elif bal_test < quantity_dollars*-2 or bal_test > quantity_dollars*3:
        elem_max = round(price_test + (price_test*0.045), round_tiker)
    else:
        elem_max = round(price_test + (price_test*0.03), round_tiker)
    print('Лімітка зверху: ',elem_max)
    return elem_max


def limit_order_min():
    bal_test = balans()
    if bal_test < quantity_dollars*-5 or bal_test > quantity_dollars*3:
        elem_min = round(price_test - (price_test*0.06), round_tiker)
    elif bal_test < quantity_dollars*-3 or bal_test > quantity_dollars*2:
        elem_min = round(price_test - (price_test*0.045), round_tiker)
    else:
        elem_min = round(price_test - (price_test*0.03), round_tiker)
    print('Лімітка знизу: ',elem_min)
    return elem_min


# Визначаємо кількість у позиції
def quantity1_long():
    bal_test = balans()
    quantity_t = round(quantity_dollars/price_test)
    if bal_test > quantity_dollars*2.1:
        quantity_long = round(10/price_test)
    elif bal_test > quantity_dollars*1.1:
        quantity_long = round((quantity_dollars*0.6)/price_test)
    else:
        quantity_long = quantity_t
    print('Кількість знизу: ',quantity_long)
    return quantity_long


def quantity1_short():
    bal_test = balans()
    quantity_t = round(quantity_dollars/price_test)
    if bal_test < quantity_dollars*-2.1:
        quantity_short = round(10/price_test)
    elif bal_test < quantity_dollars*-1.1:
        quantity_short = round((quantity_dollars*0.6)/price_test)
    else:
        quantity_short = quantity_t
    print('Кількість зверху: ',quantity_short)
    return quantity_short


# Визначаємо кількість відкритих позицій
def pozity():
    poz_t1 = len(pandas.DataFrame(client.futures_get_open_orders(symbol=tiker)))
    print('Поставлено ліміток: ', poz_t1)
    return poz_t1

#Закриваємо позицію
def clouse_pozision():
    client.futures_cancel_all_open_orders(symbol=tiker)
    open_positions = client.futures_position_information(symbol=tiker)
    for position in open_positions:
        if float(position['positionAmt']) > 0:
            side = 'SELL'
        else:
            side = 'BUY'
        quantity = abs(float(position['positionAmt']))

        # Закриття позиції
        order = client.futures_create_order(
            symbol=tiker,
            side=side,
            type='MARKET',
            quantity=quantity
        )
    print('Закрив позицію')


# Виставляємо лімітки
start_stop = True

while start_stop:
    try:
        if position_on() > quantity_dollars*-2:
            if pozity() < 2:
                price_test = last_limit_order()
                client.futures_cancel_all_open_orders(symbol=tiker)
                client.futures_create_order(
                    symbol=tiker,
                    side='SELL',
                    type='LIMIT',
                    quantity=quantity1_short(),
                    price=limit_order_max(),
                    timeInForce='GTC'
                )
                client.futures_create_order(
                    symbol=tiker,
                    side='BUY',
                    type='LIMIT',
                    quantity=quantity1_long(),
                    price=limit_order_min(),
                    timeInForce='GTC'
                )
                print('поставив лімітку short: ', limit_order_max())
                print('поставив лімітку long: ', limit_order_min())
            else:
                time.sleep(1)
                print('Чекаю')
        else:
            clouse_pozision()
            start_stop = False
    except:
        print('Помилка!')
        time.sleep(1)
