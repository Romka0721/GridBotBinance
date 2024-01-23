from binance.client import Client
from API import API_KEY, API_SEKRET
import asyncio

from bot import send_info
from settings import symbol, quantity_dollars, round_tiker

client = Client(API_KEY, API_SEKRET)


async def last_limit_order():
    trades = client.futures_account_trades(symbol=symbol)
    last_trade = float(trades[-1]['price'])
    print(last_trade)
    return last_trade


price_test = 0


# Обчислення загального балансу в позиції
async def balans():
    open_positions = client.futures_position_information(symbol=symbol)
    for position in open_positions:
        bal1 = float(position['positionAmt'])
        bal1 = round(bal1 * price_test, 1)
        print('Баланс в позиції: ', bal1)
        return bal1


# Визначання збитку в позиції
async def position_on():
    positions = client.futures_position_information(symbol=symbol)
    for position in positions:
        if position['symbol'] == symbol:
            entry_price = float(position['entryPrice'])
            mark_price = float(position['markPrice'])
            quantity = float(position['positionAmt'])
            profit = round((mark_price - entry_price) * quantity, 4)
            print('Прибуток/Збиток в позиції: ', profit)
            return profit


# Визначаємо де будуть стояти лімітки
async def limit_order_max(price_test):
    bal_test = await balans()
    if bal_test < quantity_dollars * -3 or bal_test > quantity_dollars * 5:
        elem_max = round(price_test + (price_test * 0.06), round_tiker)
    elif bal_test < quantity_dollars * -2 or bal_test > quantity_dollars * 3:
        elem_max = round(price_test + (price_test * 0.045), round_tiker)
    else:
        elem_max = round(price_test + (price_test * 0.03), round_tiker)
    print('Лімітка зверху: ', elem_max)
    return elem_max


async def limit_order_min(price_test):
    bal_test = await balans()
    if bal_test < quantity_dollars * -5 or bal_test > quantity_dollars * 3:
        elem_min = round(price_test - (price_test * 0.06), round_tiker)
    elif bal_test < quantity_dollars * -3 or bal_test > quantity_dollars * 2:
        elem_min = round(price_test - (price_test * 0.045), round_tiker)
    else:
        elem_min = round(price_test - (price_test * 0.03), round_tiker)
    print('Лімітка знизу: ', elem_min)
    return elem_min


# Визначаємо кількість у позиції
async def quantity1_long():
    bal_test = await balans()
    quantity_t = round(quantity_dollars / price_test)
    if bal_test > quantity_dollars * 3:
        quantity_long = round(10 / price_test)
    elif bal_test > quantity_dollars * 1.6:
        quantity_long = round((quantity_dollars * 0.6) / price_test)
    else:
        quantity_long = quantity_t
    print('Кількість знизу: ', quantity_long)
    return quantity_long


async def quantity1_short():
    bal_test = await balans()
    quantity_t = round(quantity_dollars / price_test)
    if bal_test < quantity_dollars * -3:
        quantity_short = round(10 / price_test)
    elif bal_test < quantity_dollars * -1.6:
        quantity_short = round((quantity_dollars * 0.6) / price_test)
    else:
        quantity_short = quantity_t
    print('Кількість зверху: ', quantity_short)
    return quantity_short


# Визначаємо кількість відкритих позицій
async def pozity():
    poz_t1 = len(client.futures_get_open_orders(symbol=symbol))
    print('Поставлено ліміток: ', poz_t1)
    return poz_t1


# Закриваємо позицію
async def clouse_pozision():
    client.futures_cancel_all_open_orders(symbol=symbol)
    open_positions = client.futures_position_information(symbol=symbol)
    for position in open_positions:
        if float(position['positionAmt']) > 0:
            side = 'SELL'
        else:
            side = 'BUY'
        quantity = abs(float(position['positionAmt']))

        # Закриття позиції
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
    print('Закрив позицію')


# Виставляємо лімітки

async def create_order_short():
    print_order = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='LIMIT',
        quantity=await quantity1_short(),
        price=await limit_order_max(price_test),
        timeInForce='GTC'
    )
    price_symbol = float(print_order['origQty'])*float(print_order['price'])
    result = (f"{print_order['symbol']}: поставив лімітку short по ціні {print_order['price']}.\n"
              f"Кількість {str(price_symbol)}")
    await send_info(result)


async def create_order_long():
    print_order = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type='LIMIT',
        quantity=await quantity1_long(),
        price=await limit_order_min(price_test),
        timeInForce='GTC'
    )
    price_symbol = float(print_order['origQty']) * float(print_order['price'])
    result = (f"{print_order['symbol']}: поставив лімітку long по ціні {print_order['price']}.\n"
              f"Кількість {str(price_symbol)}")
    await send_info(result)


async def main():
    while True:
        try:
            global price_test
            if await position_on() > quantity_dollars * -2:
                await asyncio.sleep(30)
                if await pozity() < 2:
                    await asyncio.sleep(120)
                    client.futures_cancel_all_open_orders(symbol=symbol)
                    price_test = await last_limit_order()
                    result = f'Останній закритий ордер по ціні {str(price_test)}'
                    await send_info(result)
                    await create_order_long()
                    await create_order_short()
                else:
                    print('Чекаю')
            else:
                await clouse_pozision()
                break
        except:
            print('Помилка!')
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
